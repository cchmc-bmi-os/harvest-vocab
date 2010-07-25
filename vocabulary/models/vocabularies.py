from django.db import models
from production.models.datasource import DataSourceRef
from core.models import (DiagnosisCategoryAbstract, DiagnosisAbstract, DiagnosisIndexAbstract)


class Diagnosis(DiagnosisAbstract, DataSourceRef):
    #category = models.ForeignKey('DiagnosisCategory')
    categories = models.ManyToManyField('DiagnosisCategory', 
                through='DiagnosisIndex')

    class Meta:
        app_label = u'production'
        verbose_name = u'Diagnosis'
        verbose_name_plural = u'Diagnoses'

class DiagnosisCategory(DiagnosisCategoryAbstract):
    parentCategory = models.ForeignKey('self', null=True)
    diagnoses = models.ManyToManyField(Diagnosis, through='DiagnosisIndex')
    

    class Meta:
        app_label = u'production'
        verbose_name = u'Diagnosis Category'
        verbose_name_plural = u'Diagnosis Categories'

class DiagnosisIndex(DiagnosisIndexAbstract):
    
    diagnosis = models.ForeignKey(Diagnosis)
    category = models.ForeignKey(DiagnosisCategory)
    
    class Meta:
        app_label = u'production'
        verbose_name = u'Diagnosis Index'
        verbose_name_plural = u'Diagnosis Index'
        

class VocabularyIndexAbstract(models.Model):
    """This is a generic flattened index for vocabs. It may replace the main
    model eventually"""

    level = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.id

    class Meta:
        abstract = True

class VocabularyCategoryAbstract(models.Model):
    """Vocab categories are all essentially the same, so inherit from this for specific cases"""
    name  = models.TextField(max_length=255)
    level = models.IntegerField()


    def path_to_root(self):
        """Returns a list of the parent categories to help with navigation"""
        #parents = []
        #parent_category = self
        #while parent_category.parentCategory != None:
        #    parents.append(parent_category.parentCategory)
        #    parent_category = parent_category.parentCategory
        #Reorder so the lowest index is the highest (lest-specific) category
        #parents.reverse()
        #return parents

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        abstract = True

class VocabularyItemAbstract(models.Model):
    """Vocab items are all essentially the same, so inherit from this for specifc cases"""

    def path_to_root(self):
        pass

    def __unicode__(self):
            return u'%s' % self.name

    class Meta:
        abstract = True


class DiagnosisCategoryAbstract(VocabularyCategoryAbstract):
    """Abstract model to define the hierarchy of categories for diagnoses"""

    class Meta:
        abstract = True

class DiagnosisIndexAbstract(VocabularyIndexAbstract):
    class Meta:
        abstract = True


class DiagnosisAbstract(VocabularyItemAbstract):
    """Contains a list of diagnoses organized into categories"""

    name = models.TextField(max_length=255)
    icd9 = models.TextField(null=True)

    class Meta:
        abstract = True