import os
import glob

template_dir = r"E:\agroconnect\template\supplier\*.html"
files = glob.glob(template_dir)

for file_path in files:
    # Skip files we already modernized manually
    if "service_areas.html" in file_path or "register.html" in file_path:
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    
    # Body background
    content = content.replace(
        "background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);",
        "background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://images.unsplash.com/photo-1542838132-92c53300491e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed;\n            background-size: cover;"
    )
    
    # Navbar background
    content = content.replace(
        "        .navbar {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);\n        }",
        "        .navbar {\n            background: rgba(5, 150, 105, 0.95);\n            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);\n            backdrop-filter: blur(10px);\n            border-bottom: 1px solid rgba(255, 255, 255, 0.1);\n        }"
    )
    # in case of different indentation or missing zero spacing
    content = content.replace(
        "        .navbar {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            box-shadow: 0 2px 4px rgba(0,0,0,0.1);\n        }",
        "        .navbar {\n            background: rgba(5, 150, 105, 0.95);\n            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);\n            backdrop-filter: blur(10px);\n            border-bottom: 1px solid rgba(255, 255, 255, 0.1);\n        }"
    )
    
    # Card styles
    content = content.replace(
        "        .card {\n            border: none;\n            border-radius: 15px;\n            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);\n            margin-bottom: 25px;\n        }",
        "        .card {\n            border: none;\n            border-radius: 15px;\n            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);\n            margin-bottom: 25px;\n            background: rgba(255, 255, 255, 0.98);\n        }"
    )
    content = content.replace(
        "        .card {\n            border: none;\n            border-radius: 15px;\n            box-shadow: 0 10px 25px rgba(0,0,0,0.1);\n            margin-bottom: 25px;\n        }",
        "        .card {\n            border: none;\n            border-radius: 15px;\n            box-shadow: 0 10px 25px rgba(0,0,0,0.1);\n            margin-bottom: 25px;\n            background: rgba(255, 255, 255, 0.98);\n        }"
    )

    # Card header
    content = content.replace(
        "        .card-header {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
        "        .card-header {\n            background: #059669;"
    )
    
    # Form focus
    content = content.replace(
        "        .form-control:focus {\n            border-color: #7c3aed;\n            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);\n        }",
        "        .form-control:focus {\n            border-color: #059669;\n            box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);\n        }"
    )
    content = content.replace(
        "        .form-control:focus, .form-select:focus {\n            border-color: #7c3aed;\n            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);\n        }",
        "        .form-control:focus, .form-select:focus {\n            border-color: #059669;\n            box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);\n        }"
    )
    
    # Primary button
    content = content.replace(
        "        .btn-primary {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
        "        .btn-primary {\n            background: #059669;"
    )
    
    # Primary button hover
    content = content.replace(
        "        .btn-primary:hover {\n            transform: translateY(-2px);\n            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);\n        }",
        "        .btn-primary:hover {\n            background: #047857;\n            transform: translateY(-2px);\n            box-shadow: 0 5px 15px rgba(5, 150, 105, 0.4);\n        }"
    )
    
    # Icons and text colors
    content = content.replace("color: #7c3aed;", "color: #059669;")

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {os.path.basename(file_path)}")
