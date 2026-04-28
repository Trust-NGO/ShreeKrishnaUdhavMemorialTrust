import re

filepath = r"C:\Users\ADMIN\Desktop\NGO-WEBSITE\ShreeKrishnaTrust\NGO-SITE\ShreeKrishnaUdhavMemorialTrust\backend\static\style.css"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Fix about-banner - remove negative margin, add proper padding
old_banner = """.about-banner {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-700) 100%);
  color: #fff;
  padding: 80px 0 60px;
  margin-top: calc(-1 * var(--navbar-height));
  padding-top: calc(80px + var(--navbar-height));
  text-align: center;
}"""

new_banner = """.about-banner {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-700) 100%);
  color: #fff;
  padding: 140px 0 60px;
  text-align: center;
}"""

if old_banner in content:
    content = content.replace(old_banner, new_banner)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully fixed about-banner CSS.")
else:
    print("Pattern not found in CSS.")
