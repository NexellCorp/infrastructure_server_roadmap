# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Burndown.component'
        db.add_column(u'roadmap_burndown', 'component',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Component'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Burndown.project'
        db.alter_column(u'roadmap_burndown', 'project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Project'], null=True))

    def backwards(self, orm):
        # Deleting field 'Burndown.component'
        db.delete_column(u'roadmap_burndown', 'component_id')


        # Changing field 'Burndown.project'
        db.alter_column(u'roadmap_burndown', 'project_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['roadmap.Project']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reversion.revision': {
            'Meta': {'object_name': 'Revision'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_slug': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '200', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'roadmap.burndown': {
            'Meta': {'object_name': 'Burndown'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Component']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Project']", 'null': 'True', 'blank': 'True'})
        },
        u'roadmap.burndownbar': {
            'Meta': {'object_name': 'BurndownBar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'snapshot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.BurndownSnapshot']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'roadmap.burndownsnapshot': {
            'Meta': {'object_name': 'BurndownSnapshot'},
            'burndown': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Burndown']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'roadmap.card': {
            'Meta': {'object_name': 'Card'},
            'card_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.CardType']"}),
            'components': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['roadmap.Component']", 'null': 'True', 'blank': 'True'}),
            'dependson': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'depends'", 'symmetrical': 'False', 'to': u"orm['roadmap.Card']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fix_version': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.FixVersion']", 'null': 'True', 'blank': 'True'}),
            'implementedby': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'implements'", 'symmetrical': 'False', 'to': u"orm['roadmap.Card']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['roadmap.Label']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Project']"}),
            'resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Resolution']", 'null': 'True', 'blank': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.SecurityLevel']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Status']"}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'roadmap.cardtype': {
            'Meta': {'object_name': 'CardType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'roadmap.component': {
            'Meta': {'object_name': 'Component'},
            'engineering_project': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'engineering_component'", 'unique': 'True', 'null': 'True', 'to': u"orm['roadmap.Project']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'component_set'", 'to': u"orm['roadmap.Project']"})
        },
        u'roadmap.fixversion': {
            'Meta': {'object_name': 'FixVersion'},
            'fix_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Project']", 'null': 'True', 'blank': 'True'})
        },
        u'roadmap.label': {
            'Meta': {'object_name': 'Label'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'roadmap.milestone': {
            'Meta': {'object_name': 'Milestone'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_major': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'roadmap.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'roadmap.resolution': {
            'Meta': {'object_name': 'Resolution'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Project']", 'null': 'True', 'blank': 'True'})
        },
        u'roadmap.roadmaprelease': {
            'Meta': {'object_name': 'RoadmapRelease'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release_name': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'revision': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['reversion.Revision']", 'unique': 'True'})
        },
        u'roadmap.securitylevel': {
            'Meta': {'object_name': 'SecurityLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_mandatory': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'roadmap.status': {
            'Meta': {'object_name': 'Status'},
            'display_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Project']", 'null': 'True', 'blank': 'True'}),
            'status_style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.StatusStyle']", 'null': 'True', 'blank': 'True'})
        },
        u'roadmap.statusstyle': {
            'Meta': {'object_name': 'StatusStyle'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['roadmap']