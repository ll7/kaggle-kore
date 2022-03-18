# Installation

## Conda

### Windows

Path issues:

This [link](https://stackoverflow.com/questions/44597662/conda-command-is-not-recognized-on-windows-10) does is not complete.

This [link](https://stackoverflow.com/questions/50125472/issues-with-installing-python-libraries-on-windows-condahttperror-http-000-co) is better, because it contains all three paths.

This post works perfectly to solve my problem on win7 with anaconda prompt. It basically says you need to add the following directories into your user environment path in windows (go to Start and type in: View Advanced System Settings, then select Environmental Variables: then select Path and click Edit: finally you can click New and add a path):

C:\your_directory_to_anaconda3\Anaconda3\Scripts

C:\your_directory_to_anaconda3\Anaconda3\

C:\your_directory_to_anaconda3\Anaconda3\Library\bin -- This is the directory for openssl

#### Recommended solution

This is probably the best explnation https://stackoverflow.com/a/58211115/8972010 !


## VSCode





### Extensisons

#### Github Copilot

Markdown issue https://github.com/yzhang-gh/vscode-markdown/issues/1011

```
[
  {
    "key": "tab",
    "command": "markdown.extension.onTabKey",
    "when": "editorTextFocus && !inlineSuggestionVisible && !editorReadonly && !editorTabMovesFocus && !hasOtherSuggestions && !hasSnippetCompletions && !inSnippetMode && !suggestWidgetVisible && editorLangId == 'markdown'"
  },
  {
    "key": "tab",
    "command": "-markdown.extension.onTabKey",
    "when": "editorTextFocus && !editorReadonly && !editorTabMovesFocus && !hasOtherSuggestions && !hasSnippetCompletions && !inSnippetMode && !suggestWidgetVisible && editorLangId == 'markdown'"
  }
]
```


## Environment

```
conda env create -f environment.yml
```
