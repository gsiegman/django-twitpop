# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TwitterSearchTerm'
        db.create_table('twitpop_twittersearchterm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('twitpop', ['TwitterSearchTerm'])


    def backwards(self, orm):
        
        # Deleting model 'TwitterSearchTerm'
        db.delete_table('twitpop_twittersearchterm')


    models = {
        'twitpop.twittersearchterm': {
            'Meta': {'object_name': 'TwitterSearchTerm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['twitpop']
