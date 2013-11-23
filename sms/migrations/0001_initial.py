# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'sms_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Location'], unique=True, null=True, blank=True)),
            ('subscriber', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.Subscriber'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'sms', ['Message'])

        # Adding model 'MessageTemplate'
        db.create_table(u'sms_messagetemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Status'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'sms', ['MessageTemplate'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'sms_message')

        # Deleting model 'MessageTemplate'
        db.delete_table(u'sms_messagetemplate')


    models = {
        u'accounts.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'core.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'core.status': {
            'Meta': {'object_name': 'Status'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'sms.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Location']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'subscriber': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.Subscriber']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'sms.messagetemplate': {
            'Meta': {'object_name': 'MessageTemplate'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Status']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sms']