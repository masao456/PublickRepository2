# check_template.py

import os
from django.template.loader import get_template
from django.conf import settings

# settingsに設定されたテンプレートディレクトリを表示
print(settings.TEMPLATES[0]['DIRS'])

# テンプレートが存在するかどうかを確認
template_name = 'myapp/delete_post.html'  # テンプレートのパスを指定
template_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], template_name)

if os.path.exists(template_path):
    print(f"Template '{template_name}' found at '{template_path}'")
else:
    print(f"Template '{template_name}' not found")