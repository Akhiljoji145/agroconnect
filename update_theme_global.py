import os
import glob

# Search in all subdirectories of template
template_dir = r"E:\agroconnect\template\**\*.html"
files = glob.glob(template_dir, recursive=True)
# Also get the root ones if any (though login.html is root, we filter it out)

for file_path in files:
    # Skip files we already modernized manually
    if "register.html" in file_path or "login.html" in file_path or "index.html" in file_path:
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    
    # Body background (subtle earthy/greenish background for dashboards to keep it readable instead of heavy images)
    content = content.replace(
        "background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);",
        "background: #f0fdf4;"
    )
    
    # Navbar background
    content = content.replace(
        "        .navbar {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);\n        }",
        "        .navbar {\n            background: rgba(5, 150, 105, 0.95);\n            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);\n            backdrop-filter: blur(10px);\n            border-bottom: 1px solid rgba(255, 255, 255, 0.1);\n        }"
    )
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
    
    # Button action
    content = content.replace(
        "        .btn-action {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
        "        .btn-action {\n            background: #059669;"
    )
    
    # Stats number
    content = content.replace(
        "            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            -webkit-background-clip: text;",
        "            color: #059669;"
    )

    # Some templates use color classes directly, let's fix explicit usages
    content = content.replace("color: #7c3aed;", "color: #059669;")
    content = content.replace("background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);", "background: #059669;")

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {os.path.basename(file_path)}")
