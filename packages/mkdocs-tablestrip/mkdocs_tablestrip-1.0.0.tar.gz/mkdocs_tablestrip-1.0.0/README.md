# Mkdocs Tablestrip Plugin

This plugin allows you to strip rows from tables across your documentation.
It searches for a specific heading-keyword and then removes the corresponding row from the HTML output.
The Markdown files remain unchanged.

This can be useful if your documentation contains data that is automatically parsed but not relevant for the end user.
 
## Installation
`pip install mkdocs-tablestip`

Consider adding the plugins to a `requirements.txt` file alongside other Python dependencies for your project.

## Setup
Add the plugin to your `mkdocs.yml` file:

```yaml
plugins:
  - tablestrip
```
## Configuration

There is only a single configuration option for this plugin: The keyword used to identify the row that should be removed.
```yaml
plugins:
  - tablestrip:
      strip_word: "Expert"
```
