from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Class(models.Model):
	class_name = models.CharField(max_length=45, unique=True)

	def __str__(self):
		return self.class_name

class Country(models.Model):
	country_name = models.CharField(max_length=45, unique=True)

	def __str__(self):
		return self.country_name

class Access(models.Model):
	acc_type = models.CharField(max_length=45, unique=True, verbose_name="Access Type")
	def __str__(self):
		return self.acc_type
		
class Emails(models.Model):
	email = models.EmailField()
	owner = models.IntegerField()
	group = models.IntegerField()
	def __str__(self):
		return self.email

class Category(models.Model):
	cat_type = models.CharField(max_length=45, unique=True, verbose_name="Category Type")
	def __str__(self):
		return self.cat_type

class Cennostatus(models.Model):
	cns = models.CharField(max_length=45, unique=True, verbose_name="Center No. Registration status")
	def __str__(self):
		return self.cns

class Level(models.Model):
	lev_name = models.CharField(max_length=45, unique=True, verbose_name="Level")
	def __str__(self):
		return self.lev_name

class Subject(models.Model):
	name = models.CharField(max_length=45, unique=True,)
	subject_level = models.ManyToManyField(Level,)
	def __str__(self):
		return self.name

class Ownership(models.Model):
	own_type = models.CharField(max_length=45, unique=True, verbose_name="Ownership Type")
	def __str__(self):
		return self.own_type

class Region(models.Model):
	reg_name = models.CharField(max_length=45, unique=True, verbose_name="Region")
	def __str__(self):
		return self.reg_name

class District(models.Model):
	dis_name = models.CharField(max_length=45, unique=True, verbose_name="District Name")
	region = models.ForeignKey(Region, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="Region")
	def __str__(self):
		return self.dis_name

class Regstatus(models.Model):
	rs_type = models.CharField(max_length=45, unique=True, verbose_name="Registration status")
	def __str__(self):
		return self.rs_type

class County(models.Model):
	county_name = models.CharField(max_length=45, unique=True, verbose_name="County")
	def __str__(self):
		return self.county_name

class SubCounty(models.Model):
	subcounty_name = models.CharField(max_length=45, unique=True, verbose_name="Sub-County")
	def __str__(self):
		return self.subcounty_name

class Parish(models.Model):
	parish_name = models.CharField(max_length=45, verbose_name="Parish")
	district = models.ForeignKey(District, on_delete = models.SET_NULL, blank=True, null=True,)
	county = models.ForeignKey(County, on_delete = models.SET_NULL, blank=True, null=True,)
	subcounty = models.ForeignKey(SubCounty, on_delete = models.SET_NULL, blank=True, null=True,)

	def __str__(self):
		return f'{self.parish_name}, {self.subcounty}, {self.county}, {self.district}'

class Schtype(models.Model):
	sch_type = models.CharField(max_length=45, unique=True, verbose_name="School Type")
	def __str__(self):
		return self.sch_type

class Section(models.Model):
	sec_type = models.CharField(max_length=45, unique=True, verbose_name="Section")
	def __str__(self):
		return self.sec_type

class Funder(models.Model):
	funder_name = models.CharField(max_length=45, unique=True, verbose_name="Funder")
	def __str__(self):
		return self.funder_name

class TertiaryLevel(models.Model):
	level_name = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.level_name

class TertiaryCategory(models.Model):
	category_name = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.category_name

class DistanceToNearestSchool(models.Model):
	distance = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.distance

class DistanceToDeoOffice(models.Model):
	distance = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.distance

class RuralUrban(models.Model):
	rural_urban = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.rural_urban


class School(models.Model):
	name = models.CharField(max_length=100, verbose_name="School Name")
	motto = models.CharField(max_length=100, blank=True, null=True, verbose_name="School Motto")
	address = models.CharField(max_length=100, blank=True, null=True,)
	box_no = models.CharField(max_length=100, blank=True, null=True,)
	website = models.CharField(max_length=100, blank=True, null=True,)
	phone = models.CharField(max_length=15, blank=True, null=True,)
	fax = models.CharField(max_length=100, blank=True, null=True,)
	service_code = models.CharField(max_length=100, blank=True, null=True,)
	email = models.EmailField(blank=True, null=True)
	reg_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Registration Number")
	cen_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Center Number")
	yr_est = models.IntegerField(blank=True, null=True, verbose_name="Year Established")
	yr_reg = models.IntegerField(blank=True, null=True, verbose_name="Year of Registration")
	yr_cnr = models.IntegerField(blank=True, null=True, verbose_name="Year of Center No. Registration")
	access = models.ForeignKey(Access, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="School Access")
	category = models.ForeignKey(Category, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="School Category")
	cennostatus = models.ForeignKey(Cennostatus, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="Center No. Registration status")
	regstatus = models.ForeignKey(Regstatus, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="Registration status")
	level = models.ForeignKey(Level, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="Highest Level")
	founder = models.ForeignKey(Ownership, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="Founding Body")
	section = models.ForeignKey(Section, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="Section")
	operation_status = models.ForeignKey(Schtype, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="School Type")
	parish = models.ForeignKey(Parish, on_delete = models.SET_NULL, blank=True, null=True,)
	funder = models.ForeignKey(Funder, on_delete = models.SET_NULL, blank=True, null=True,)
	tertiary_level = models.ForeignKey(TertiaryLevel, on_delete = models.SET_NULL, blank=True, null=True,)
	tertiary_category = models.ForeignKey(TertiaryCategory, on_delete = models.SET_NULL, blank=True, null=True,)
	distance_to_nearest_school = models.ForeignKey(DistanceToNearestSchool, on_delete = models.SET_NULL, blank=True, null=True,)
	distance_to_deo_office = models.ForeignKey(DistanceToDeoOffice, on_delete = models.SET_NULL, blank=True, null=True,)
	rural_urban = models.ForeignKey(RuralUrban, on_delete = models.SET_NULL, blank=True, null=True,)
	highest_class = models.ForeignKey(Class, on_delete = models.SET_NULL, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	logo = models.ImageField(default='school_logos/default.png', upload_to='school_logos', blank=True, null=True,)
	def __str__(self):
		return self.name

class TeacherResponsibility(models.Model):
	responsibility = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.responsibility

class TeacherEducation(models.Model):
	education_level = models.CharField(max_length=45, unique=True, )
	def __str__(self):
		return self.education_level

class TeacherProfession(models.Model):
	profession = models.CharField(max_length=45, unique=True, )
	def __str__(self):
		return self.profession

class TeacherSalaryScale(models.Model):
	profession = models.CharField(max_length=45, unique=True, )
	def __str__(self):
		return self.profession

class TeacherTraining(models.Model):
	training = models.CharField(max_length=45, unique=True, )
	def __str__(self):
		return self.training

class Gender(models.Model):
	gender = models.CharField(max_length=45, unique=True, verbose_name="Gender")
	def __str__(self):
		return self.gender

class FacilityType(models.Model):
	facility_type = models.CharField(max_length=45, unique=True, verbose_name="Facility Type")
	def __str__(self):
		return self.facility_type

class FacilityStatus(models.Model):
	facility_status = models.CharField(max_length=45, unique=True, verbose_name="Facility status")
	def __str__(self):
		return self.facility_status
class TeacherStatus(models.Model):
	teacher_status = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.teacher_status

class ResourceType(models.Model):
	resource_type = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.resource_type

class ResourceSource(models.Model):
	resource_source = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.resource_source

class Resource(models.Model):
	resource_type = models.ForeignKey(ResourceType, on_delete = models.CASCADE)
	source = models.ForeignKey(ResourceSource, on_delete = models.SET_NULL, blank=True, null=True,)
	description = models.CharField(max_length=200)
	quantity = models.IntegerField()
	amount = models.IntegerField()
	year = models.DateField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	photo = models.ImageField(default='default.png', upload_to='teacher_photos')
	def __str__(self):
		return self.description

class AllocateResource(models.Model):
	resource = models.ForeignKey(Resource, on_delete = models.CASCADE)
	school = models.ForeignKey(School, on_delete = models.CASCADE)
	quantity = models.IntegerField()
	amount = models.IntegerField()
	year = models.DateField(default=timezone.now)
	date_allocated = models.DateField(default=timezone.now)
	date_valid = models.DateField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	def __str__(self):
		return f'{self.resource} to {self.school}'

class Facility(models.Model):
	facility_type = models.ForeignKey(FacilityType, on_delete = models.CASCADE)
	school = models.ForeignKey(School, on_delete = models.CASCADE)
	status = models.ForeignKey(FacilityStatus, on_delete = models.SET_NULL, blank=True, null=True,)
	description = models.CharField(max_length=200)
	quantity = models.CharField(max_length=45)
	photo = models.ImageField(default='default.png', upload_to='fac_uploads')
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	def __str__(self):
		return self.facility_type

class Teacher(models.Model):
	surname = models.CharField(max_length=200,)
	first_name = models.CharField(max_length=200,)
	school = models.ForeignKey(School, blank=True, null=True, on_delete = models.SET_NULL, verbose_name="Current School")
	payroll_number = models.CharField(max_length=11, blank=True, null=True,)
	phone = models.CharField(max_length=13, blank=True, null=True,)
	nin = models.CharField(max_length=14, blank=True, null=True,)
	email = models.EmailField(blank=True, null=True)
	on_payroll = models.BooleanField(default=True,)
	status = models.ForeignKey(TeacherStatus, default=1, on_delete = models.SET_DEFAULT, verbose_name="Teacher Status")
	gender = models.ForeignKey(Gender, on_delete = models.SET_NULL, blank=True, null=True,)
	responsibilities = models.ManyToManyField(TeacherResponsibility, blank=True,)
	specialization = models.ManyToManyField(Subject, related_name="specialization", blank=True,)
	taught = models.ManyToManyField(Subject, related_name="taught", blank=True,)
	dob = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
	first_posting = models.DateField(blank=True, null=True, verbose_name="Date of first posting")
	first_appointment = models.DateField(blank=True, null=True, verbose_name="Date of first appointment")
	district = models.ForeignKey(District, on_delete = models.SET_NULL, blank=True, null=True, related_name="district")
	previous_post = models.ForeignKey(District, on_delete = models.SET_NULL, blank=True, null=True, related_name="previous_post")
	education = models.ForeignKey(TeacherEducation, on_delete = models.SET_NULL, blank=True, null=True,)
	profession = models.ForeignKey(TeacherProfession, on_delete = models.SET_NULL, blank=True, null=True,)
	salary_scale = models.ForeignKey(TeacherSalaryScale, on_delete = models.SET_NULL, blank=True, null=True,)
	training = models.ForeignKey(TeacherTraining, on_delete = models.SET_NULL, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	photo = models.ImageField(default='teacher_photos/default.png', upload_to='teacher_photos', blank=True, null=True,)
			
	def __str__(self):
		return f'{self.surname} {self.first_name}'

class TransferTeacher(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
	school = models.ForeignKey(School, on_delete = models.CASCADE, related_name='school_to')
	school_from = models.ForeignKey(School, on_delete = models.CASCADE, related_name='school_from')
	designation = models.ForeignKey(TeacherResponsibility, default=1, on_delete = models.SET_DEFAULT, blank=True, null=True,)
	date_valid = models.DateField(blank=True, null=True, verbose_name="Transfer Teacher Until")
	date_transfered = models.DateTimeField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	def __str__(self):
		return f'{self.teacher} to {self.school}'

class SchoolTeacher(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE, related_name='teacher')
	current = models.ForeignKey(School, on_delete = models.CASCADE, related_name='current')
	previous = models.ForeignKey(School, on_delete = models.CASCADE, related_name='previous')
	def __str__(self):
		return f'{self.teacher} to {self.current}'

class Deo(models.Model):
	name = models.CharField(max_length=200, verbose_name="Deo's Name")
	email = models.EmailField(blank=True, null=True)
	status = models.ForeignKey(TeacherStatus, default=1, on_delete = models.SET_DEFAULT, verbose_name="Deo Status")
	gender = models.ForeignKey(Gender, on_delete = models.SET_NULL, blank=True, null=True,)
	district = models.ForeignKey(District, on_delete = models.SET_NULL, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	photo = models.ImageField(default='default.png', upload_to='deo_photos')
			
	def __str__(self):
		return self.name

class TransferDeo(models.Model):
	deo = models.ForeignKey(Deo, on_delete = models.CASCADE)
	district = models.ForeignKey(District, on_delete = models.CASCADE)
	date_valid = models.DateField(blank=True, null=True, verbose_name="Transfer Deo Until")
	date_transfered = models.DateTimeField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	def __str__(self):
		return f'{self.deo} to {self.district}'

class ProductStatus(models.Model):
	status = models.CharField(max_length=200, unique=True,)
	def __str__(self):
		return self.status

class Product(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	price = models.IntegerField()
	phone_contact = models.IntegerField()
	status = models.ForeignKey(ProductStatus, default=1, on_delete = models.SET_DEFAULT, verbose_name="Product Status")
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	photo = models.ImageField(default='default.png', upload_to='product_photos')
	def __str__(self):
		return self.title
		
class ProductVote(models.Model):
	vote = models.IntegerField()
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

class TeacherCategory(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class NewTeacher(models.Model):
	name = models.CharField(max_length=200)
	reg_no = models.CharField(max_length=200, unique=True)
	category = models.ForeignKey(TeacherCategory, on_delete = models.SET_NULL, blank=True, null=True,)
	subject = models.ForeignKey(Subject, on_delete = models.SET_NULL, blank=True, null=True,)
	def __str__(self):
		return self.reg_no

class SchoolRankPLE(models.Model):
	rank = models.IntegerField()
	div1 = models.IntegerField()
	div2 = models.IntegerField()
	div3 = models.IntegerField()
	div4 = models.IntegerField()
	year = models.IntegerField()
	school = models.CharField(max_length=200)
	def __str__(self):
		return f'{self.school}'

class SchoolRankUCE(models.Model):
	rank = models.IntegerField()
	div1 = models.IntegerField()
	div2 = models.IntegerField()
	div3 = models.IntegerField()
	div4 = models.IntegerField()
	year = models.IntegerField()
	school = models.CharField(max_length=200)
	def __str__(self):
		return f'{self.school}'

class SchoolRankUACE(models.Model):
	rank = models.IntegerField()
	number = models.IntegerField()
	year = models.IntegerField()
	school = models.CharField(max_length=200)
	def __str__(self):
		return f'{self.school}'


