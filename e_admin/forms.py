from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from wtforms import SelectMultipleField, Form
from flask_login import current_user
from flask.ext.sauth.models import User, authenticate
from e_organisation.models import *


class AddOrganisationForm( Form):
    org_name =TextField( validators=[v.DataRequired(), v.Length(max=255)])
    branches =TextField()
    states =TextField( )
    areas =TextField( )
    regions =TextField( )
    postal_address =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_telephone =TextField( validators=[v.DataRequired(), v.Length(max=20)])
    postal_tele_code =TextField( validators=[v.DataRequired(), v.Length(max=5)])
    postal_code =TextField( validators=[v.DataRequired(), v.Length(max=10)])
    postal_country =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_state =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_city =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    email =TextField( validators=[v.DataRequired(), v.Email(), v.Length(max=256), v.Email()])

    def validate_org_name(form, field):
        org_name = field.data.lower().strip()
        if EsthenosOrg.objects(name=org_name).count():
            raise ValidationError("Hey! This organisation is already registered with us")

    def save(self):
        settings = EsthenosSettings.objects.all()[0]
        org = EsthenosOrg(name=self.org_name.data, code = ""+str(settings.organisations_count))
        org.postal_address =self.postal_address.data
        org.postal_telephone =self.postal_telephone.data
        org.postal_tele_code =self.postal_tele_code.data
        org.postal_country =self.postal_country.data
        org.postal_state =self.postal_state.data
        org.postal_city =self.postal_city.data
        org.postal_code = self.postal_code.data
        org.email = self.email.data
        org.owner = EsthenosUser.objects.get(id=current_user.id)

        org.save()
        return org


class AddEmployeeForm(Form):
    FirstName =TextField( validators=[v.DataRequired(), v.Length(max=255)])
    LastName =TextField( validators=[v.DataRequired(), v.Length(max=512)])
    role =TextField( validators=[v.DataRequired(), v.Length(max=512)])
    DateOfBirth=TextField( validators=[v.DataRequired(), v.Length(max=512)])
    gender =TextField( validators=[v.DataRequired(), v.Length(max=12)])
    Address =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    TeleNo =TextField( validators=[v.DataRequired(), v.Length(max=20)])
    TeleCode =TextField( validators=[v.DataRequired(), v.Length(max=5)])
    City = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    State = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    Country = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    PostalCode = TextField(validators=[v.DataRequired(),v.Length(max=6)])

    Email = TextField(validators=[v.DataRequired(), v.Email(), v.Length(max=256)])
    Password = PasswordField(validators=[v.DataRequired(),v.Length(max=30)])

    def save(self):
        emp = EsthenosUser.create_user(self.FirstName.data,self.Email.data,self.Password.data,True)
        emp.active = True
        emp.sex = self.gender.data
        emp.email = self.Email.data
        emp.last_name = self.LastName.data
        emp.first_name = self.FirstName.data
        emp.roles.append(self.role.data)
        emp.date_of_birth = self.DateOfBirth.data
        emp.postal_address = self.Address.data
        emp.postal_telephone = self.TeleNo.data
        emp.postal_tele_code = self.TeleCode.data
        emp.postal_city = self.City.data
        emp.postal_state = self.State.data
        emp.postal_country = self.Country.data
        emp.owner = EsthenosUser.objects.get(id=current_user.id)
        emp.save()
        return emp


class RegistrationFormAdmin( Form):
    type = HiddenField()
    name = TextField( validators=[v.DataRequired(), v.Length(max=256)])
    email = TextField( validators=[v.DataRequired(), v.Email(), v.Length(max=256)])
    password = PasswordField( validators=[v.DataRequired(), v.Length(max=256)])

    def validate_email(form, field):
        email = field.data.lower().strip()
        if EsthenosUser.objects(email=email).count():
            raise ValidationError( "Hey! This email is already registered with us. Did you forget your password?")

    def save(self):
        user = EsthenosUser.create_user( self.name.data, self.email.data, self.password.data, email_verified=True)
        user.save()
        return user


class AddOrganizationEmployeeForm(Form):
    last_name_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    first_name_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])

    active = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    gender = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    date_of_birth_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])

    email_add_organisation = TextField( validators=[v.DataRequired(), v.Email(), v.Length(max=256)])
    password_add_organisation = PasswordField(validators=[v.DataRequired(), v.Length(max=30)])

    role = TextField( validators=[v.DataRequired(), v.Length(max=255)])

    address_add_org_emp = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    city_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    state_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    country_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    teleno_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    tele_code_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    postal_code_add_organisation = TextField( validators=[v.DataRequired(), v.Length(max=255)])

    states = SelectMultipleField('states')
    regions = SelectMultipleField('regions')
    areas = SelectMultipleField('areas')
    branches = SelectMultipleField('branches')
    centers = SelectMultipleField('centers')

    def validate_email_add_organisation(form, field):
        email_add_organisation = field.data.lower().strip()
        if EsthenosUser.objects(email=email_add_organisation).count():
            raise ValidationError( "Hey! This email is already registered with us. Did you forget your password?")

    def save(self, org_id):
        emp = EsthenosUser.create_user(self.first_name_add_organisation.data,
                                       self.email_add_organisation.data,
                                       self.password_add_organisation.data)

        emp.last_name = self.last_name_add_organisation.data
        emp.first_name = self.first_name_add_organisation.data

        emp.email = self.email_add_organisation.data
        emp.gender = self.gender.data
        emp.active = True if self.active.data == "active" else False

        emp.date_of_birth = self.date_of_birth_add_organisation.data
        emp.postal_address = self.address_add_org_emp.data
        emp.postal_code = self.postal_code_add_organisation.data
        emp.postal_city = self.city_add_organisation.data
        emp.postal_state = self.state_add_organisation.data
        emp.postal_country = self.country_add_organisation.data
        emp.postal_telephone = self.teleno_add_organisation.data
        emp.postal_tele_code = self.tele_code_add_organisation.data

        emp.hierarchy = EsthenosOrgHierarchy.objects.get(id=self.role.data)
        emp.organisation = EsthenosOrg.objects.get(id=org_id)
        emp.save()

        org = EsthenosOrg.objects.get(id=org_id)
        org.update(inc__employee_count=1)
        return emp

    def update(self, emp):
        emp.last_name = self.last_name_add_organisation.data
        emp.first_name = self.first_name_add_organisation.data
        emp.gender = self.gender.data
        emp.active = True if self.active.data == "active" else False

        emp.date_of_birth = self.date_of_birth_add_organisation.data
        emp.postal_address = self.address_add_org_emp.data
        emp.postal_code = self.postal_code_add_organisation.data
        emp.postal_city = self.city_add_organisation.data
        emp.postal_state = self.state_add_organisation.data
        emp.postal_country = self.country_add_organisation.data
        emp.postal_telephone = self.teleno_add_organisation.data
        emp.postal_tele_code = self.tele_code_add_organisation.data

        emp.hierarchy = EsthenosOrgHierarchy.objects.get(id=self.role.data)

        to_save = True

        selections = []
        #todo centralize the level assignments
        if emp.hierarchy.level == 3:
            for state in self.states.data:
                state = EsthenosOrgState.objects.get(id=state)
                regions = map(lambda r: str(r.id), state.regions)
                commons = set.intersection(set(regions), self.regions.data)
                print state.owner
                if not len(commons) and state.owner == None:
                    state.owner = emp
                    state.save()
                    selections.append(state)
            if len(selections)<1:
                to_save = False
        emp.states = selections

        selections = []
        #todo centralize the level assignments
        if emp.hierarchy.level == 4:
            for region in self.regions.data:
                region = EsthenosOrgRegion.objects.get(id=region)
                areas = map(lambda r: str(r.id), region.areas)
                commons = set.intersection(set(areas), self.areas.data)
                if not len(commons) and region.owner == None:
                    region.owner = emp
                    region.save()
                    selections.append(region)
            if len(selections)<1:
                to_save = False
        emp.regions = selections

        selections = []
        #todo centralize the level assignments
        if emp.hierarchy.level == 5:
            for area in self.areas.data:
                area = EsthenosOrgArea.objects.get(id=area)
                branches = map(lambda r: str(r.id), area.branches)
                commons = set.intersection(set(branches), self.branches.data)
                if not len(commons) and area.owner == None:
                    area.owner = emp
                    area.save()
                    selections.append(area)
            if len(selections)<1:
                to_save = False
        emp.areas = selections

        selections = []
        #todo centralize the level assignments
        if emp.hierarchy.level >= 6:
            for branch in self.branches.data:
                branch = EsthenosOrgBranch.objects.get(id=branch)
                centers = map(lambda r: str(r.id), branch.centers)
                commons = set.intersection(set(centers), self.centers.data)
                if not len(commons):
                    if emp.hierarchy.level == 6 and branch.owner == None:
                        branch.owner = emp
                        branch.save()
                        selections.append(branch)
                    if emp.hierarchy.level == 7:
                        selections.append(branch)
            if len(selections)<1:
                to_save = False
        emp.branches = selections

        selections = []
        #todo centralize the level assignments
        if emp.hierarchy.level == 7:
            for center in self.centers.data:
                selections.append(EsthenosOrgCenter.objects.get(id=center))
        emp.centers = selections

        if len(emp.branches)>1 and emp.hierarchy.level == 7:
            to_save = False

        if to_save:
            emp.save()

        return emp

class AddOrganisationProductForm( Form):
    product_name=TextField( validators=[v.Length(max=255)])
    loan_type=TextField( validators=[v.Length(max=255)])
    loan_amount=TextField( validators=[ v.Length(max=255)])
    life_insurance=TextField( validators=[ v.Length(max=255)])
    eligible_cycle=TextField( validators=[ v.Length(max=255)])
    number_installments=TextField( validators=[ v.Length(max=255)])
    emi=TextField( validators=[ v.Length(max=255)])
    last_emi=TextField( validators=[ v.Length(max=255)])
    service_tax=TextField( validators=[ v.Length(max=255)])
    insurance_service_tax=TextField( validators=[ v.Length(max=255)])
    processing_fee=TextField( validators=[ v.Length(max=255)])
    total_processing_fees=TextField( validators=[ v.Length(max=255)])
    interest_rate=TextField( validators=[ v.Length(max=255)])
    insurance_period=TextField( validators=[ v.Length(max=255)])
    insurance_free=TextField( validators=[ v.Length(max=255)])
    total_insurance_fees=TextField( validators=[ v.Length(max=255)])
    emi_repayment=TextField( validators=[ v.Length(max=255)])
    rd_fee=TextField( validators=[ v.Length(max=255)])

    def validate_product_name(form,field):
        product_name =field.data.lower().strip()
        if( EsthenosOrgProduct.objects.filter(product_name=product_name).count()):
            raise ValidationError( "Hey! This product is already registered with us")

    def save( self,org_id):
        prod=EsthenosOrgProduct(product_name=self.product_name.data)
        prod.loan_amount=float(self.loan_amount.data)
        prod.loan_type = self.loan_type.data
        prod.life_insurance=float(self.life_insurance.data)
        prod.eligible_cycle=int(self.eligible_cycle.data)
        prod.number_installments=int(self.number_installments.data)
        prod.emi=float(self.emi.data)
        prod.service_tax=float(self.service_tax.data)
        prod.insurance_service_tax=float(self.insurance_service_tax.data)
        prod.last_emi=float(self.last_emi.data)
        prod.processing_fee=float(self.processing_fee.data)
        prod.total_processing_fees=float(self.total_processing_fees.data)
        prod.interest_rate=float(self.interest_rate.data)
        prod.insurance_free=float(self.insurance_free.data)
        prod.insurance_period=float(self.insurance_period.data)
        prod.total_insurance_fees=float(self.total_insurance_fees.data)
        prod.emi_repayment=self.emi_repayment.data
        prod.rd_fee=self.rd_fee.data
        prod.organisation=EsthenosOrg.objects.get(id=org_id)
        prod.save()
        return prod


class AddOrgPsychometricTemplateQuestionsForm( Form):
    org_id = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    question = TextField( validators=[v.DataRequired(), v.Length(max=2048)])
    question_hindi = TextField( validators=[v.DataRequired(), v.Length(max=2048)])

    answer1 = TextField ( validators=[v.DataRequired(), v.Length(max=2048)])
    answer_regional1 = TextField (validators=[v.DataRequired(), v.Length(max=2048)])

    answer2 = TextField ( validators=[v.DataRequired(), v.Length(max=2048)])
    answer_regional2 = TextField (validators=[v.DataRequired(), v.Length(max=2048)])

    answer3 = TextField ( validators=[v.DataRequired(), v.Length(max=2048)])
    answer_regional3 = TextField (validators=[v.DataRequired(), v.Length(max=2048)])

    answer4 = TextField ( validators=[v.DataRequired(), v.Length(max=2048)])
    answer_regional4 = TextField (validators=[v.DataRequired(), v.Length(max=2048)])

    def save( self):
        ques=EsthenosOrgPsychometricTemplateQuestion()
        ques.question=self.question.data
        ques.question_regional = self.question_hindi.data

        ques.answer1 = self.answer1.data
        ques.answer_regional1 = self.answer_regional1.data

        ques.answer2 = self.answer2.data
        ques.answer_regional2 = self.answer_regional2.data

        ques.answer3 = self.answer3.data
        ques.answer_regional3 = self.answer_regional3.data

        ques.answer4 = self.answer4.data
        ques.answer_regional4 = self.answer_regional4.data

        ques.organisation=EsthenosOrg.objects.get(id=self.org_id.data)
        ques.save()
        return ques
