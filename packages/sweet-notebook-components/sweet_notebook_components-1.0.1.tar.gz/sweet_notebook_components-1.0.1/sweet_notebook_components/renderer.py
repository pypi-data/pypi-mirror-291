class Renderer:
    def render_to_html(self, json) -> str:

        return f"""<script id="sweet-notebook-components-data" type="application/json">{json}</script>
<div id="sweet-notebook-components-root"></div>
<script>
  console.log('Hello from renderer');
</script>
"""
