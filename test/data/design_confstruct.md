Design
######

definitions
-----------
## def-cs::structure
a class that is aware of its members and can be used to store a set of attributes.

## def-cs::attribute
"this structure is composed of attributes. Each attribute has: a name, a description, a validity and a target variable of any **compatible variable type**"


## def-compatible-file-types
compatible file type

### def-json format
JSON format

### def-xml-format
XML format

### def-yaml-format
XML format


## def-compatible variable type
compatible variable type

### def-variable-type1
read from a subset of a **compatible text file type**

### def-variable-type2
validated against a range

requirements
------------
## general

### reqQQQ
A cs::structure can be read from an input file of any **compatible text file type**

### reqQQQ
A cs::structure can be written to an output file of any **compatible text file type**

### reqQQQ
A cs::structure can be reset to its default value


### reqQQQ
A cs::structure can be validated ; the validity criterion is given for each cs::attribute

### reqQQQ
A cs::structure can be documented
#- inheritance

### reqQQQ
a child cs::structure shall inherit the list of cs::attribute of the parent cs::structure

### reqQQQ
a cs::structure can contain a child cs::attribute inside a parent cs::attribute type (abstract or concrete)
#- compatible type

### reqQQQ
all fundamental type is a **compatible type**

### reqQQQ
std::string is a **compatible type**

### reqQQQ
a class enum is a **compatible type**

### reqQQQ
a std::list of any **compatible type** is a **compatible type**

### reqQQQ
a std::map of any **compatible type** is a **compatible type**

### reqQQQ
a class or structure containing classes of any **compatible type** is a **compatible type** (they must be objects and not references/pointers)

### reqQQQ
a custom class designed by the user can become a **compatible type**

