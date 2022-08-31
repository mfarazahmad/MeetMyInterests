import React from 'react'
import dynamic from 'next/dynamic';

const Editor = dynamic(
    () => import('react-draft-wysiwyg').then(mod => mod.Editor),
    { ssr: false }
)

const BlogEditor = (props) => {

    return (
        <Editor
            editorState={props.post}
            toolbarClassName="toolbarClassName"
            wrapperClassName="wrapperClassName"
            editorClassName="editorClassName"
            onEditorStateChange={props.handleEditor}
        />
    )
}

export default BlogEditor