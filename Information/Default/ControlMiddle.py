import Modules.Imports as Imports

test_format = "\t\\drawpage{{{control_event} №{event_number}\\\\по дисциплине <<Аналитическая геометрия>>}}{{{group}}}{{{student}}}{{\n{excercises}\n\t}}\n"
excercise_format = "\t\t\\item {title}\n{tasks}"
tasks_format = "\t\t\t{task}" 

LayoutLocation = "Layouts/control_middle_layout.tex"

PageStyle = Imports.Documents.PageStyle(test_format, excercise_format, tasks_format)