# streamlit-page-link-params

An alternative to the official Streamlit page_link component that supports query parameters.

## Installation instructions

Requirements: streamlit >= 1.37, Python >= 3.8

```sh
pip install streamlit-page-link-params
```

## Usage instructions

### Basic, no params
```
page_link("pages/p1.py", label="go to p1")
```

### Basic, use_container_width=True, with params: use_container_width=true
```
page_link("pages/p1.py", label="go to p1", use_container_width=True, query_params={"use_container_width": "true"})
```

### use html, with params: html=true
```
page_link_html('<a href="/p1" style="font-size: 30px;">go to p1</a>', query_params={{"html": "true"}})
```

### use html, with style, with params: html=true&with_style=color
```
page_link_html("""
<style>
.myPageLink {
    color: green !important;
}
</style>
<a href="/p1" class="myPageLink">go to p1</a>
""", query_params={"html": "true", "with_style": "color"})
```
