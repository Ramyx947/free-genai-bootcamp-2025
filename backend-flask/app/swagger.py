from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Romanian Learning API"}
)

# Example swagger.json content to be placed in static/swagger.json
"""
{
  "openapi": "3.0.0",
  "info": {
    "title": "Romanian Learning API",
    "description": "API for managing Romanian vocabulary with AI-powered content generation "
    "and safety guardrails",
    "version": "1.0.0"
  },
  "paths": {
    "/api/vocabulary": {
      "post": {
        "summary": "Generate vocabulary with AI",
        "description": "Uses AI to generate vocabulary with guardrails for content safety and quality",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/VocabularyRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Vocabulary generated successfully",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/VocabularyResponse"
                }
              }
            }
          },
          "400": {
            "description": "Invalid input or guardrails validation failure",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/GuardrailsError"
                }
              }
            }
          }
        },
        "tags": ["Vocabulary"]
      }
    }
  },
  "components": {
    "schemas": {
      "GuardrailsError": {
        "type": "object",
        "properties": {
          "success": {
            "type": "boolean",
            "example": false
          },
          "error": {
            "type": "string",
            "example": "Input contains inappropriate content"
          },
          "details": {
            "type": "object",
            "properties": {
              "reason": {
                "type": "string",
                "example": "Content violates community guidelines"
              }
            }
          }
        }
      }
    }
  }
}
"""

swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "Romanian Language Learning API",
        "description": "API for managing vocabulary and learning sessions",
        "version": "1.0.0",
    },
    "basePath": "/api",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "paths": {
        "/dashboard": {
            "get": {
                "tags": ["Dashboard"],
                "summary": "Get dashboard statistics",
                "description": "Returns learning progress and statistics",
                "responses": {
                    "200": {
                        "description": "Dashboard data",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "stats": {
                                    "type": "object",
                                    "properties": {
                                        "total_words": {"type": "integer"},
                                        "learned_words": {"type": "integer"},
                                        "active_groups": {"type": "integer"},
                                    },
                                }
                            },
                        },
                    }
                },
            }
        },
        "/words": {
            "get": {
                "tags": ["Words"],
                "summary": "Get all words",
                "description": "Returns a list of all vocabulary words",
                "responses": {
                    "200": {
                        "description": "List of words",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "success": {"type": "boolean"},
                                "data": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "romanian": {"type": "string"},
                                            "english": {"type": "string"},
                                            "pronunciation": {"type": "string"},
                                            "part_of_speech": {"type": "string"},
                                            "parts": {"type": "string"},
                                        },
                                    },
                                },
                            },
                        },
                    }
                },
            }
        },
        "/groups": {
            "get": {
                "tags": ["Groups"],
                "summary": "Get all word groups",
                "description": "Returns a list of all vocabulary groups",
                "responses": {
                    "200": {
                        "description": "List of groups",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "success": {"type": "boolean"},
                                "data": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "name": {"type": "string"},
                                            "description": {"type": "string"},
                                            "wordCount": {"type": "integer"},
                                        },
                                    },
                                },
                            },
                        },
                    }
                },
            },
            "post": {
                "tags": ["Groups"],
                "summary": "Create a new word group",
                "description": "Creates a new vocabulary group",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                            },
                            "required": ["name"],
                        },
                    }
                ],
                "responses": {"201": {"description": "Group created successfully"}},
            },
        },
    },
}
