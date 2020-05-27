## Install  
`pip install git+https://github.com/hudikm/PatchCreator.git`

## Usage 
TODO
### Git diff customization
File: `.gitattributes`

Content:<br>
*.java  diff=java
*.c     diff=cpp
*.cpp   diff=cpp
[Git docs](https://git-scm.com/docs/gitattributes#_defining_a_custom_hunk_header)

### Example
`patchcreator.py --git-path="/src/main/" HouseHoldService out.patch`
