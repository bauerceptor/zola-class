# themes/neovim-theme — VENDOR INSTRUCTIONS

The Neovim theme is NOT included in this repo as a submodule.
It is vendored (copied in directly) so upstream changes never break your site.

## One-time setup

Run these commands from the repo2 root:

```bash
# Clone the theme into a temp location
git clone https://github.com/Super-Botman/neovim-theme /tmp/neovim-theme

# Record the commit hash for your records (paste it into config.toml)
cd /tmp/neovim-theme && git rev-parse HEAD

# Copy the theme files into this repo
cp -r /tmp/neovim-theme/* themes/neovim-theme/

# Remove the .git directory so it is not treated as a submodule
rm -rf themes/neovim-theme/.git

# Stage everything
cd /path/to/zola-class
git add themes/neovim-theme
git commit -m "vendor: add neovim-theme at commit HASH"
```

## What goes in here after setup

```
themes/neovim-theme/
├── theme.toml
├── templates/
│   ├── base.html
│   ├── index.html
│   └── ...
├── static/
│   ├── css/
│   └── js/
└── ...
```

## Checking the hook name for _head_extend.html

After vendoring, open `themes/neovim-theme/templates/base.html` and search
for the block that loads extra head content. Common names are:

  {% block extra_head %}
  {% block head_extra %}
  {% block custom_head %}

Update `templates/_head_extend.html` to extend the correct block name.
If the theme uses a direct `{% include %}` instead, add your includes there.

## Updating the theme

To update: re-run the clone/copy steps above with the new commit.
Record the new hash in config.toml. Test locally before pushing.
