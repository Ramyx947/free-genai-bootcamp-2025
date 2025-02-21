from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from .config import Config
from .swagger import swagger_config

# HTML template for the root endpoint
API_DOCS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Romanian Language Learning API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 0 20px;
        }
        .endpoint {
            background: #f5f5f5;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #2196F3;
        }
        .endpoint h3 {
            margin: 0 0 10px 0;
            color: #2196F3;
        }
        .endpoint p {
            margin: 5px 0;
            color: #666;
        }
        .endpoint a {
            color: #2196F3;
            text-decoration: none;
        }
        .endpoint a:hover {
            text-decoration: underline;
        }
        .method {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            background: #e0e0e0;
            margin-right: 10px;
        }
        #response-container {
            display: none;
            margin-top: 20px;
        }
        #response-data {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            white-space: pre-wrap;
            font-family: monospace;
        }
        .back-button {
            background: #2196F3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .back-button:hover {
            background: #1976D2;
        }
        #endpoints-list {
            transition: all 0.3s ease;
        }
    </style>
</head>
<body>
    <div id="endpoints-list">
        <h1>Romanian Language Learning API</h1>
        <p>Welcome to the API. Choose how you want to explore:</p>
        
        <div class="endpoint">
            <h3><a href="/docs">Interactive API Documentation (Swagger UI)</a></h3>
            <p>Test the API endpoints with an interactive interface</p>
        </div>

        <div class="endpoint">
            <h3><a href="#" onclick="showEndpoints(); return false;">Simple Endpoint Tester</a></h3>
            <p>Quick test of API endpoints with simple responses</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span><a href="/api/health">/api/health</a></h3>
            <p>Check API health status</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span><a href="/api/words">/api/words</a></h3>
            <p>Get all vocabulary words from the database</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span><a href="/api/dashboard">/api/dashboard</a></h3>
            <p>Get dashboard statistics and information</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span><a href="/api/groups">/api/groups</a></h3>
            <p>Get all word groups</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span><a href="/api/groups">/api/groups</a></h3>
            <p>Create a new word group</p>
        </div>
    </div>

    <div id="response-container">
        <button class="back-button" onclick="showEndpoints()">← Back to Endpoints</button>
        <h2 id="response-url"></h2>
        <pre id="response-data"></pre>
    </div>

    <script>
        const endpointsList = document.getElementById('endpoints-list');
        const responseContainer = document.getElementById('response-container');
        const responseUrl = document.getElementById('response-url');
        const responseData = document.getElementById('response-data');

        function showEndpoints() {
            responseContainer.style.display = 'none';
            endpointsList.style.display = 'block';
            // Update URL without refreshing
            history.pushState({}, '', '/');
        }

        function showResponse() {
            responseContainer.style.display = 'block';
            endpointsList.style.display = 'none';
        }

        // Handle browser back button
        window.onpopstate = function(event) {
            showEndpoints();
        };

        document.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', async (e) => {
                e.preventDefault();
                try {
                    const response = await fetch(link.href);
                    const data = await response.json();
                    
                    // Update display
                    responseUrl.textContent = `Response from ${link.href}`;
                    responseData.textContent = JSON.stringify(data, null, 2);
                    showResponse();

                    // Update URL without refreshing
                    history.pushState({}, '', link.href);
                } catch (error) {
                    console.error('Error fetching data:', error);
                    alert('Error fetching data. Check console for details.');
                }
            });
        });
    </script>
</body>
</html>
"""

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Disable strict slashes
    app.url_map.strict_slashes = False

    # Register Swagger UI blueprint
    SWAGGER_URL = '/docs/'
    API_URL = '/static/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Romanian Language Learning API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Serve swagger spec
    @app.route("/static/swagger.json/")
    def specs():
        return jsonify(swagger_config)

    # Register API blueprints
    from .routes import dashboard_bp, words_bp, groups_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard/')
    app.register_blueprint(words_bp, url_prefix='/api/words/')
    app.register_blueprint(groups_bp, url_prefix='/api/groups/')

    @app.route('/')
    def root():
        return render_template_string(API_DOCS_TEMPLATE)

    @app.route('/api/health/')
    def health_check():
        return {"status": "healthy", "message": "API is running"}

    return app
