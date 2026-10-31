"""
Flask Application for Computing History Agent Client.

This is the main Flask application that provides a web interface
for interacting with the Computing History agent.
"""

from flask import Flask, render_template, request, jsonify
import markdown
import bleach
from agent_client import AgentClient

app = Flask(__name__)

# Image uploads: PNG and JPEG only, up to 5 MB
MAX_IMAGE_BYTES = 5 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = MAX_IMAGE_BYTES + 1024 * 1024  # allow for form overhead


def detect_image_type(data: bytes):
    """Identify PNG or JPEG data from its file signature (do not trust the client content type)."""
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if data.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    return None


def _set_external_link_attributes(attrs, new=False):
    """Force safe external link attributes for rendered markdown links."""
    href_key = (None, 'href')
    href_value = attrs.get(href_key, '')
    if isinstance(href_value, str) and href_value.startswith(('http://', 'https://')):
        attrs[(None, 'target')] = '_blank'
        attrs[(None, 'rel')] = 'noopener noreferrer nofollow'
    return attrs


def render_markdown_to_safe_html(text: str) -> str:
    """Convert markdown to safe HTML for display in chat bubbles."""
    raw_html = markdown.markdown(
        text,
        extensions=['extra', 'sane_lists', 'nl2br']
    )

    allowed_tags = [
        'p', 'br', 'hr', 'blockquote',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li',
        'strong', 'em', 'code', 'pre',
        'a',
        'table', 'thead', 'tbody', 'tr', 'th', 'td'
    ]
    allowed_attrs = {
        'a': ['href', 'title', 'target', 'rel'],
        'code': ['class']
    }

    safe_html = bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=['http', 'https', 'mailto'],
        strip=True
    )

    # Linkify plain URLs while leaving code blocks untouched.
    safe_html = bleach.linkify(
        safe_html,
        skip_tags=['pre', 'code'],
        callbacks=[_set_external_link_attributes]
    )
    return safe_html

# Initialize the agent client
try:
    agent = AgentClient()
except Exception as e:
    print(f"Warning: Failed to initialize agent client: {e}")
    agent = None

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the user."""
    if not agent:
        return jsonify({
            'error': 'Agent client not initialized. Check your .env configuration.'
        }), 500
    
    # Accept multipart form data (text plus an optional image) or plain JSON (text only)
    if request.mimetype == 'multipart/form-data':
        user_message = request.form.get('message', '').strip()
        image_file = request.files.get('image')
    else:
        data = request.get_json(silent=True) or {}
        user_message = data.get('message', '').strip()
        image_file = None
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Validate message length to prevent abuse
    if len(user_message) > 10000:
        return jsonify({'error': 'Message too long'}), 400
    
    # Validate the optional image
    image_data = None
    image_media_type = None
    if image_file and image_file.filename:
        image_data = image_file.read(MAX_IMAGE_BYTES + 1)
        if len(image_data) > MAX_IMAGE_BYTES:
            return jsonify({'error': 'Image is too large. The maximum size is 5 MB.'}), 400
        image_media_type = detect_image_type(image_data)
        if not image_media_type:
            return jsonify({'error': 'Unsupported image type. Use a PNG or JPEG image.'}), 400
    
    # Note: We do NOT escape HTML here because:
    # 1. The agent needs to receive the raw text to understand it properly
    # 2. HTML escaping is performed on the frontend when displaying messages
    # 3. This follows the principle: escape at the point of use (display), not at input
    response = agent.send_message(user_message, image_data, image_media_type)
    response_html = render_markdown_to_safe_html(response)

    return jsonify({
        'response': response,
        'response_html': response_html
    })

@app.errorhandler(413)
def request_too_large(e):
    """Return a JSON error when an upload exceeds the size limit."""
    return jsonify({'error': 'Image is too large. The maximum size is 5 MB.'}), 413

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the conversation history."""
    if agent:
        agent.reset_conversation()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=False, port=5000)
