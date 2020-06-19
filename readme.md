### Introduction

The creation of a step-by-step tutorial is a time-consuming process.
Utility `patchcreator` in conjunction with `tutgen.py` are tools to ease up this process.
This tools can generate step-by-step tutorials from git repository.

- [`patchcreator`](https://github.com/hudikm/PatchCreator) will create patch file from git repository
- [`tutgen.py`](https://github.com/hudikm/TutGen) will generate code snippets from patch file. By default a code snippets are created in markdown format supported by [MkDocs material template](https://squidfunk.github.io/mkdocs-material/). Snippet generation is done with use of Jinja2 templates, so it can be customized to almost any output format.     

Tutorial example: [TrafficCounter](https://hudikm.github.io/TrafficCounterDemo/) ([Source](https://github.com/hudikm/TrafficCounterDemo/tree/docs))

**1. Create a git repository with step-by-step code**

Generated steps in tutorial are produced from individual commits.
Every commit should represent a logical changes in code that need to be made to create a certain step. A commit message need to be formatted: `STEP NO. step title`

Example of git commit messages:
```
2.1 Observe LiveData objects
2.0 Use LiveData in ViewModel class
1.4 Use the ViewModel in your UI Controller
1.3 Associate the UI Controller and ViewModel
1.2 Add lifecycle-extensions to the project
IGNORE this commit is ignored
1.1 Create a ViewModel class
1.0 Basic functionality
Init commit
```
If commit is tagged as `IGNORE` than it will be ignored. 

If repository is pushed on github than every step will have a link to the committed version on github.   

**2. Create a patch file from repository**

> Android example:
> ```
> patchcreator.py --git-path="app/src/main/java app/build.gradle" . out.patch
> ```

**3. Generate steps**

The snippets are generated in markdown language that will be processed by [MkDocs](https://www.mkdocs.org/) documentation static site generator supplemented by [MkDocs material template](https://squidfunk.github.io/mkdocs-material/).

Example of `index.md` that will generate all snippet placeholders:
```
<!--tgen file='out.patch' lang=java tabs t_new="New" t_old="Old" -->
<!--tgen step=all template='gen_tags_separate_header' remove -->
<!--end-->
```

Run the command:
```shell script
tutGen.py index.md
```
Result: 
```
<!--tgen file='out.patch' lang=java tabs t_new="New" t_old="Old" -->
<!--tgen step=all template='gen_tags_separate_header'  -->
<!--tgen step=1.0 template='mkdocs_header_only'  -->
<!--end-->

<!--tgen step=1.0 template='mkdocs_body_only'  -->
<!--end-->

<!--tgen step=1.1 template='mkdocs_header_only'  -->
<!--end-->

<!--tgen step=1.1 template='mkdocs_body_only'  -->
<!--end-->

...
                                                                                 
<!--tgen step=2.2 template='mkdocs_header_only'  -->                                                                                 
<!--end-->

<!--tgen step=2.2 template='mkdocs_body_only'  -->
<!--end-->

<!--end-->

```

Run the command `tutGen.py index.md` again that now will generate code snippets.  


## Install  
- Patch creator: `pip install git+https://github.com/hudikm/PatchCreator.git`
- TutGen: `pip install git+https://github.com/hudikm/TutGen.git`

## Requirements
- Python 3.6
- [MkDocs](https://www.mkdocs.org/) + [material template](https://squidfunk.github.io/mkdocs-material/) (if you don't want to use mkdocs you need change jinja templates that are used to generate snippets)

## Usage 
```
usage: patchcreator.py [-h] [-e [encoding]] [--git-path [git_path]]
                       gitdir [outfile]

Generate patch file

positional arguments:
  gitdir                Location of git repo.
  outfile

optional arguments:
  -h, --help            show this help message and exit
  -e [encoding], --encoding [encoding]
                        Encodning default: utf8
  --git-path [git_path] 
                        When paths are given, show them (note that this isn’t
                        really raw pathnames, but rather a list of patterns to
                        match). Otherwise implicitly uses the root level of
                        the tree as the sole path argument. Example:
                        "app/src/main/res/layout/ app/src/main/java/"

```
```
usage: tutGen.py [-h] [-d [diff_file]] [-e [encoding]] [-t [template]]
                 [-v [VERBOSE]]
                 infile [outfile]

Generate code snippets from diff file

positional arguments:
  infile                Input file to process
  outfile               Output file

optional arguments:
  -h, --help            show this help message and exit
  -d [diff_file], --diff_file [diff_file]
                        Git diff file/url
  -e [encoding], --encoding [encoding]
                        Encodning
  -t [template], --template [template]
                        Template file
  -v [VERBOSE], --verbose [VERBOSE]
                        Verbose mode

```
### Git diff customization

Patchcreator use git diff command in background to create output patch file. Command git diff can by customized by providing
the file `.gitattributes`. This file can be placed globally or locally([link](https://stackoverflow.com/questions/28026767/where-should-i-place-my-global-gitattributes-file?answertab=active#tab-top)) 

**Defining a custom hunk-header**

Settings example of specific language definition for git diff ([Git docs](https://git-scm.com/docs/gitattributes#_defining_a_custom_hunk_header))
```
*.java  diff=java
*.c     diff=cpp
*.cpp   diff=cpp
```

### TutGen Tags
Tag is defined as html comment `<!--tgen -->` and when it is used as placeholder it need to have end tag `<!--end-->` 

Tags are divided into two groups:
 1. tags defining global context
 2. tags using global context   

**Tags defining global context** need to define `file` attribute

`<!--tgen file='' lang="" tabs t_new="" t_old="" context="" prefix="" suffix="" nohighlight headerRegex-->`

Attributes defined in global context tag will define default values in tags using this context.

| attribute   | description                                           | default value      | mandatory |
| ----------- | ----------------------------------------------------- | ------------------ | --------- |
| file        | path to patch file                                    |                    | Yes       |
| context     | if used multiple patch files this defines new context | main context       | No        |
| tabs        | use of tabs (code before and after change)            | false              | No        |
| t_new       | tab title                                             | "New"              | No        |
| t_old       | tab title                                             | "Old"              | No        |
| lang        | language for highlighting                             |                    | No        |
| nohighlight | turn off highlighting                                 | highlighting is on | No        |
| prefix      | step prefix                                           |                    | No        |
| suffix      | step suffix                                           |                    | No        |
| headerRegex |                                                       |                    |           |

**Tags using global context**

Attributes defined in tag will overwrite the default context values

| attribute   | description                                                  | default value      | mandatory |
| ----------- | ------------------------------------------------------------ | ------------------ | --------- |
| step        | define steps that will be placed in this placeholder: <br>single step: 1.0<br>multiple steps: 1.0,1.1,2.0<br>range of steps: 1.0-2.0<br>all steps: all |                    | yes       |
| context     | if used multiple patch files this defines to witch context tag belongs | main context       | No        |
| tabs        | use of tabs (code before and after change)                   | false              | No        |
| t_new       | tab title                                                    | "New"              | No        |
| t_old       | tab title                                                    | "Old"              | No        |
| lang        | language for highlighting                                    |                    | No        |
| nohighlight | turn off highlighting                                        | highlighting is on | No        |
| prefix      | step prefix                                                  |                    | No        |
| suffix      | step suffix                                                  |                    | No        |
| headerRegex |                                                              |                    | No        |
| visibility  | Possible values: all, tag, title, none                       | all                | No        |
| append      | append the code snipped to existing content in placeholder   | False              | No        |
| noupdate    | existing content in placeholder will not be change           | False              | No        |
| remove      | placeholder tag will be removed, only the code snipped remains | False              | No        |

### Templates

```
files_list.jinja
gen_tags.jinja
gen_tags_separate_header.jinja
mkdocs.jinja
mkdocs_body.jinja
mkdocs_body_only.jinja
mkdocs_header.jinja
mkdocs_header_only.jinja
mkdocs_content.jinja
```