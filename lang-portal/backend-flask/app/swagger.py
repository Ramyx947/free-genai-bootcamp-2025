swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "Romanian Language Learning API",
        "description": "API for managing vocabulary words and study sessions",
        "version": "1.0.0"
    },
    "basePath": "/api",
    "schemes": [
        "http"
    ],
    "paths": {
        "/words/": {
            "get": {
                "tags": ["Words"],
                "summary": "Get all vocabulary words",
                "responses": {
                    "200": {
                        "description": "List of words"
                    }
                }
            }
        },
        "/groups/": {
            "get": {
                "tags": ["Groups"],
                "summary": "Get all word groups",
                "responses": {
                    "200": {
                        "description": "List of groups"
                    }
                }
            },
            "post": {
                "tags": ["Groups"],
                "summary": "Create a new group",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "example": "Fruits"
                                },
                                "description": {
                                    "type": "string",
                                    "example": "Romanian fruit vocabulary"
                                }
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Group created successfully"
                    }
                }
            }
        },
        "/health/": {
            "get": {
                "tags": ["System"],
                "summary": "Check API health",
                "responses": {
                    "200": {
                        "description": "Health status"
                    }
                }
            }
        }
    }
} 