import EditorJS from '@editorjs/editorjs';
import Header from '@editorjs/header';
import List from '@editorjs/list';
import Paragraph from '@editorjs/paragraph';
import ImageTool from '@editorjs/image'
import Delimiter from '@editorjs/delimiter'
import InlineCode from '@editorjs/inline-code'

export default function invokeEditorJS(id, data){

const editor = new EditorJS({
    holder: id,
    logLevel: 'ERROR',
    data: data,
    tools: {
         header: {
          class: Header,
          inlineToolbar: ['link']
        },
        list: {
          class: List,
          inlineToolbar: true
        },
        paragraph: {
            class: Paragraph,
            inlineToolbar: true
        },
        image: {
          class: ImageTool,
          config: {
            endpoints: {
              byFile: window.byf, // Your backend file uploader endpoint
              byUrl: window.byu, // Your endpoint that provides uploading by Url
            },
            additionalRequestHeaders: {
                "X-CSRFToken": window.csrfToken
            }
          }
        },
        delimiter: Delimiter,
        inlineCode: {
          class: InlineCode,
          shortcut: 'CMD+SHIFT+M',
        },
    }
});

return editor

}
