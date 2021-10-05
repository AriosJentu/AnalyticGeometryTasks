import random

from ..Default import Homework
import Modules.Imports as Imports

from ..Scripts import Lines

control_event = "Индивидуальное домашнее задание"
event_number = 2

prefix = "Tasks/Homework2/"

def tasks_updater(text):
	
	sprod2 = Lines.ScalarProduct(2)
	sprod3 = Lines.ScalarProduct(3)

	sprod2.generate_random_vectors()
	text = text.replace("#SCALARS#", sprod2.to_vectors_form())

	sprod2.generate_random_vectors()
	text = text.replace("#SCALARLENGTH1#", sprod2.to_length_scalar_product_form())
	
	sprod2.generate_random_vectors()
	text = text.replace("#SCALARLENGTH2#", sprod2.to_length_scalar_product_form())
	
	sprod2.generate_random_vectors()
	text = text.replace("#SCALARPRODUCT#", sprod2.to_scalar_product_form())
	
	sprod2.generate_random_vectors()
	text = text.replace("#SCALARPRODUCTLINEAR#", sprod2.to_linear_scalar_product_form())
	
	sprod2.generate_random_vectors()
	sprod3.generate_random_vectors()
	text = text.replace("#SCALARANGLE1#", sprod2.to_lengths_form())
	text = text.replace("#SCALARANGLE2#", sprod3.to_lengths_form())
	
	sprod3.generate_random_vectors()
	text = text.replace("#SCALARPROD3#", sprod3.to_scalar_product_form())
	
	sprod3.generate_random_vectors()
	text = text.replace("#SCALARPROD3LENGTH#", sprod3.to_linear_scalar_product_form())



	return text

tasks = []
for i in range(5):
	tasks_i = Imports.Tasks.SpecificTasks()
	task_i = Imports.Tasks.SpecificTaskInfo(prefix+f"Task{i+1}.tex")
	task_i.set_updater_function(tasks_updater)
	tasks_i.append(task_i)
	tasks.append(tasks_i)

tasksinfo = []
for task in tasks:
	taskinfo = [Imports.Tasks.TasksInformation(task)]
	tasksinfo.append(taskinfo)

exercises = []
for taskinfo in tasksinfo:
	exercise = Imports.Excercises.Excercise(taskinfo)
	exercises.append(exercise)

class Homework2(Imports.Assignments.Assignment):

	layout = Imports.Documents.DocumentLayout(Homework.LayoutLocation, Homework.PageStyle)
	test = Imports.Tests.Test(exercises)
	document_entries = Imports.Entries.DocumentEntries(control_event=control_event, event_number=event_number)
	prefix = "ageom_hw"
	number = event_number

