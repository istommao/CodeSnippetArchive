import React from 'react'
import BraftEditor from 'braft-editor'
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import 'braft-editor/dist/index.css'
import 'braft-extensions/dist/code-highlighter.css'
import CodeHighlighter from 'braft-extensions/dist/code-highlighter'

import 'prismjs/components/prism-java'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-php'
import styles from './index.less';

// 通过opitons.
const options = {
  syntaxs: [
    {
      name: 'JavaScript',
      syntax: 'javascript'
    }, {
      name: 'HTML',
      syntax: 'html'
    }, {
      name: 'CSS',
      syntax: 'css'
    }, {
      name: 'Python',
      syntax: 'python'
    }, {
      name: 'Java',
      syntax: 'java',
    }, {
      name: 'PHP',
      syntax: 'php'
    }
  ],
  includeEditors: ['editor-with-code-highlighter']
}

BraftEditor.use(CodeHighlighter(options))

// BraftEditor.use(CodeHighlighter({
//   includeEditors: ['editor-with-code-highlighter'],
// }))


export default class EditorDemo extends React.Component {

  state = {
      editorState: null
  }

  async componentDidMount () {
    // Assume here to get the editor content in html format from the server
    const htmlContent = ''; //await fetchEditorContent()
    // Use BraftEditor.createEditorState to convert html strings to editorState data needed by the editor
    this.setState({
      editorState: BraftEditor.createEditorState(htmlContent)
    })
  }

  submitContent = async () => {
    // Pressing ctrl + s when the editor has focus will execute this method
    // Before the editor content is submitted to the server, you can directly call editorState.toHTML () to get the HTML content
    const htmlContent = this.state.editorState.toHTML()
    const result = await saveEditorContent(htmlContent)
  }

  handleEditorChange = (editorState) => {
    this.setState({ editorState })
  }

  render () {

    const { editorState } = this.state

    return (
      <PageHeaderWrapper>
       <div className={ styles.editor}>
        <BraftEditor id="editor-with-code-highlighter"/>
      </div>
      </PageHeaderWrapper>
    )

  }

}
