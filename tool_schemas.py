TOOLS = [

    # DATABASE TOOLS
    {
        "type": "function",
        "function": {
            "name": "get_user",
            "description": "Get user information by user ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_user",
            "description": "Add a new user to the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "country": {"type": "string"}
                },
                "required": ["username", "email", "country"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_user",
            "description": "Remove a user by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_all_users",
            "description": "List all users in the database",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_duplicates",
            "description": "Remove duplicate users based on email",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    # FILE TOOLS

    {
        "type": "function",
        "function": {
            "name": "read_txt",
            "description": "Read contents of a text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_excel",
            "description": "Read contents of an Excel file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"}
                },
                "required": ["filepath"]
            }
        }
    }
]
