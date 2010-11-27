;; define templates for some boilerplate code
;; this uses tempoMode in emacs 

(tempo-define-template "biblatexproperty"
'((p "Attribute: " attribute) 
  " = FieldProperty(IBiblatexEntry['" 
  (s attribute) "'])" > n > r)
"fpr"
"Insert biblatex fieldproperty.")

(tempo-define-template "biblatexfield"
'((p "Attribute: " attribute)
  " = field."(p "Schema: ")"(" > n 
  > r "title = _('zblx-"(s attribute)"-tit', u'"(p "Title: ")"')," > n
  > r "description = _('zblx-"(s attribute)"-desc', u'''"(p "Description: ")"''')," > n
  > r "required = False," > n
  > r ")" > n > n > r)
"fld"
"Insert biblatex field schema.")


