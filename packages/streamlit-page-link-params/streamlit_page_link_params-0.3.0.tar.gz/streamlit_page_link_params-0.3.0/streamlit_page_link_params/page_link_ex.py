import base64
import json
import logging
import os
import re
import time

import streamlit as st
from streamlit.errors import StreamlitAPIException
from streamlit.file_util import get_main_script_directory, normalize_path_join
from streamlit.runtime.scriptrunner.script_runner import get_script_run_ctx

from streamlit_event_hook import st_listen, render_interceptor
from streamlit_js_callback import streamlit_js_callback

_CONTAINER_CLASS = "page-link-d78avs"
_SESSION_STATE_KEY = "__streamlit-page-params"
_SESSION_STATE_JUMP_DATA = f"{_SESSION_STATE_KEY}.page_params"
_JUMP_COMPONENT_KEY = f"{_SESSION_STATE_KEY}.{time.time()}"


def _page_link_style():
    st.markdown('''
        <style class="myPageLinkStyle">
        .element-container:has(.stMarkdown .myPageLinkStyle ) {
            display: none;
        }

        .my-emotion-cache-5mpj3n:active, .my-emotion-cache-5mpj3n:visited, .my-emotion-cache-5mpj3n:hover {
            text-decoration: none;
        }

        .my-emotion-cache-j7qwjs {
            display: flex;
            flex-direction: column;
        }

        .my-emotion-cache-1bjvju3 {
            text-decoration: none;
            width: fit-content;
            display: flex;
            flex-direction: row;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: start;
            justify-content: flex-start;
            gap: 0.5rem;
            border-radius: 0.25rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            margin-top: 0.125rem;
            margin-bottom: 0.125rem;
            line-height: 2;
            background-color: transparent;
        }

        .my-emotion-cache-1bjvju3:active, .my-emotion-cache-1bjvju3:visited, .my-emotion-cache-1bjvju3:hover {
            text-decoration: none;
        }
        .my-emotion-cache-1bjvju3:hover {
            background-color: rgba(172, 177, 195, 0.15);
        }

        /* use_container_width  */
        .my-emotion-cache-5mpj3n {
            text-decoration: none;
            display: flex;
            flex-direction: row;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: start;
            justify-content: flex-start;
            gap: 0.5rem;
            border-radius: 0.25rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            margin-top: 0.125rem;
            margin-bottom: 0.125rem;
            line-height: 2;
            background-color: transparent;
        }

        .my-emotion-cache-5mpj3n:hover {
            background-color: rgba(172, 177, 195, 0.15);
        }

        .my-emotion-cache-1dj0hjr {
            color: rgb(250, 250, 250);
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
            display: table-cell;
        }

        .my-emotion-cache-fm8pe0 {
            font-family: "Source Sans Pro", sans-serif;
        }

        .my-emotion-cache-fm8pe0 p {
            word-break: break-word;
            margin-bottom: 0px;
        }

        .myLink {
            color: #4285f4;
            text-decoration: none;
            word-wrap: break-word;
        }
        .myPointer {
            cursor: pointer;
        }
        </style>
        ''', unsafe_allow_html=True)


@st.fragment
def _listen_jump():
    global _JUMP_COMPONENT_KEY
    jump_target = streamlit_js_callback("""
    function findParentWithClass(element, classNameFragment) {
        while (element) {
            // 检查当前元素是否是 <div> 且 class 包含 "my"
            if (element.tagName.toUpperCase() === 'DIV' && element.className.includes(classNameFragment)) {
                return element;
            }
            // 向上查找父级元素
            element = element.parentElement;
            if (element === null || element === undefined) {
                break
            }
        }
        return null; // 如果没有找到匹配的元素，返回 null
    }

    const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));
    (async function() {
        for (let i=0; i<20; i++) {
            window.parent.document.querySelectorAll('.page-link-d78avs').forEach((item) => {
                if (item.getAttribute('data-listen') !== 'true') {
                    item.setAttribute('data-listen', 'true');
                    // console.log("add event", item);
                    item.querySelector('a').addEventListener('click', (e) => {
                        // console.log("click", e.target);
                        const targetElement = findParentWithClass(e.target, 'page-link-d78avs');
                        // console.log("page element", targetElement.getAttribute('data-page'), targetElement)
                        sendMessage(targetElement.getAttribute('data-page'))
                    })
                }
            })
            await sleep(500)
        }
    })()
    """, key=_JUMP_COMPONENT_KEY)
    if jump_target:
        jump_data = json.loads(base64.b64decode(jump_target))
        logging.info(f"Jump to page: `{jump_data}`")
        st.session_state[_SESSION_STATE_JUMP_DATA] = jump_data
        _JUMP_COMPONENT_KEY = f"{_SESSION_STATE_KEY}.{time.time()}"
        st.switch_page(jump_data["path"])


def _set_query_params(remove_jump_data=False):
    jump_data = st.session_state.get(_SESSION_STATE_JUMP_DATA)
    if jump_data and jump_data["params"] is not None:
        ctx = get_script_run_ctx()
        current_page_hash = str(ctx.pages_manager.get_current_page_script_hash())
        if current_page_hash == jump_data["hash"]:
            logging.info(f"Jump by page link params, {jump_data}")
            st.query_params.from_dict(jump_data["params"])
        if remove_jump_data:
            del st.session_state[_SESSION_STATE_JUMP_DATA]


@render_interceptor("before")
def _before():
    _page_link_style()
    _set_query_params()


@render_interceptor("after")
def _after():
    _listen_jump()
    _set_query_params(remove_jump_data=True)


def init_():
    st_listen()


def _gen_default_html_code(label, use_container_width=False):
    use_container_width_style = "my-emotion-cache-5mpj3n" if use_container_width else "my-emotion-cache-1bjvju3"
    return f"""
    <div class="my-emotion-cache-j7qwjs">
        <a data-testid="stPageLink-NavLink" href="#" rel="noreferrer" 
        class="{use_container_width_style} myPointer">
            <span class="myLink e11k5jya0">
                <div data-testid="stMarkdownContainer" class="my-emotion-cache-fm8pe0">
                    <p>{label}</p>
                </div>
            </span>
        </a>
    </div>
    """


def _gen_component(page_path, page_hash, code, params=None):
    page_data = base64.b64encode(
        json.dumps({"path": page_path, "hash": page_hash, "params": params}).encode("utf8")).decode("utf8")
    return st.html(f"""
    <div class="{_CONTAINER_CLASS}" data-page="{page_data}">
        {code}
    </div>
    """)


def _match_page(page: str) -> (str, str):
    """
    获取页面的相对路径

    :param page: page file path or url path, such as: pages/p1.py or /p1

    :return (page path, page hash)
    """
    ctx = get_script_run_ctx()
    all_app_pages = ctx.pages_manager.get_pages().values()
    main_script_directory = get_main_script_directory(ctx.main_script_path)
    if page.endswith(".py"):
        requested_page = os.path.realpath(
            normalize_path_join(main_script_directory, page)
        )
        matched_page = filter(lambda p: p["script_path"] == requested_page, all_app_pages)
    else:
        requested_page = page.strip("/")
        matched_page = filter(lambda p: p["page_name"] == requested_page, all_app_pages)
    matched_page = next(matched_page, None)
    if not matched_page:
        raise StreamlitAPIException(
            f"Could not find page: `{page}`. Must be the file path relative to the main script, from the directory: `{os.path.basename(main_script_directory)}`. Only the main app file and files in the `pages/` directory are supported."
        )
    matched_page_path = os.path.relpath(matched_page['script_path'], main_script_directory)
    matched_page_hash = str(matched_page['page_script_hash'])
    return matched_page_path, matched_page_hash


def page_link(page: str, label, use_container_width=False, query_params=None):
    """

    :param page: 页面文件的相对路径或者页面的URL路径
    """
    if not isinstance(page, str):
        raise StreamlitAPIException("Page must be a string, file path or url path")
    (page_path, page_hash) = _match_page(page)

    return _gen_component(page_path, page_hash, _gen_default_html_code(label, use_container_width), query_params)


def page_link_html(html, query_params=None):
    """
    自定义点击的页面，需带有a标签以及href，href内容为跳转页面的URL路径
    """
    res = re.findall(r'<a\s+[^>]*href="([^"]*)"', html)
    if len(res) == 0 or len(res) > 1:
        raise StreamlitAPIException("html must contain only one link.")
    (page_path, page_hash) = _match_page(res[0])
    html = re.sub(r'(<a\s+[^>]*href=)"([^"]*)"', r'\1"#"', html)
    return _gen_component(page_path, page_hash, html, query_params)
