# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Burndown'
        db.create_table(u'roadmap_burndown', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Project'])),
        ))
        db.send_create_signal(u'roadmap', ['Burndown'])

        # Adding model 'BurndownSnapshot'
        db.create_table(u'roadmap_burndownsnapshot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('burndown', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Burndown'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'roadmap', ['BurndownSnapshot'])

        # Adding model 'BurndownBar'
        db.create_table(u'roadmap_burndownbar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snapshot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.BurndownSnapshot'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'roadmap', ['BurndownBar'])

        # Adding model 'CardType'
        db.create_table(u'roadmap_cardtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'roadmap', ['CardType'])

        # Adding model 'Milestone'
        db.create_table(u'roadmap_milestone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_major', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'roadmap', ['Milestone'])

        # Adding model 'SecurityLevel'
        db.create_table(u'roadmap_securitylevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('login_mandatory', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'roadmap', ['SecurityLevel'])

        # Adding model 'Project'
        db.create_table(u'roadmap_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'roadmap', ['Project'])

        # Adding model 'RoadmapRelease'
        db.create_table(u'roadmap_roadmaprelease', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reversion.Revision'], unique=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('release_name', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal(u'roadmap', ['RoadmapRelease'])

        # Adding model 'FixVersion'
        db.create_table(u'roadmap_fixversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('fix_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Project'], null=True, blank=True)),
        ))
        db.send_create_signal(u'roadmap', ['FixVersion'])

        # Adding model 'Resolution'
        db.create_table(u'roadmap_resolution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Project'], null=True, blank=True)),
        ))
        db.send_create_signal(u'roadmap', ['Resolution'])

        # Adding model 'StatusStyle'
        db.create_table(u'roadmap_statusstyle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal(u'roadmap', ['StatusStyle'])

        # Adding model 'Status'
        db.create_table(u'roadmap_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('status_style', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.StatusStyle'], null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Project'], null=True, blank=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'roadmap', ['Status'])

        # Adding model 'Component'
        db.create_table(u'roadmap_component', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='component_set', to=orm['roadmap.Project'])),
            ('engineering_project', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='engineering_component', unique=True, null=True, to=orm['roadmap.Project'])),
        ))
        db.send_create_signal(u'roadmap', ['Component'])

        # Adding model 'Label'
        db.create_table(u'roadmap_label', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'roadmap', ['Label'])

        # Adding model 'Card'
        db.create_table(u'roadmap_card', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=128, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Status'])),
            ('resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Resolution'], null=True, blank=True)),
            ('fix_version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.FixVersion'], null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.Project'])),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.SecurityLevel'], null=True, blank=True)),
            ('card_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roadmap.CardType'])),
        ))
        db.send_create_signal(u'roadmap', ['Card'])

        # Adding M2M table for field components on 'Card'
        m2m_table_name = db.shorten_name(u'roadmap_card_components')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm[u'roadmap.card'], null=False)),
            ('component', models.ForeignKey(orm[u'roadmap.component'], null=False))
        ))
        db.create_unique(m2m_table_name, ['card_id', 'component_id'])

        # Adding M2M table for field implementedby on 'Card'
        m2m_table_name = db.shorten_name(u'roadmap_card_implementedby')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_card', models.ForeignKey(orm[u'roadmap.card'], null=False)),
            ('to_card', models.ForeignKey(orm[u'roadmap.card'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_card_id', 'to_card_id'])

        # Adding M2M table for field dependson on 'Card'
        m2m_table_name = db.shorten_name(u'roadmap_card_dependson')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_card', models.ForeignKey(orm[u'roadmap.card'], null=False)),
            ('to_card', models.ForeignKey(orm[u'roadmap.card'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_card_id', 'to_card_id'])

        # Adding M2M table for field labels on 'Card'
        m2m_table_name = db.shorten_name(u'roadmap_card_labels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm[u'roadmap.card'], null=False)),
            ('label', models.ForeignKey(orm[u'roadmap.label'], null=False))
        ))
        db.create_unique(m2m_table_name, ['card_id', 'label_id'])


    def backwards(self, orm):
        # Deleting model 'Burndown'
        db.delete_table(u'roadmap_burndown')

        # Deleting model 'BurndownSnapshot'
        db.delete_table(u'roadmap_burndownsnapshot')

        # Deleting model 'BurndownBar'
        db.delete_table(u'roadmap_burndownbar')

        # Deleting model 'CardType'
        db.delete_table(u'roadmap_cardtype')

        # Deleting model 'Milestone'
        db.delete_table(u'roadmap_milestone')

        # Deleting model 'SecurityLevel'
        db.delete_table(u'roadmap_securitylevel')

        # Deleting model 'Project'
        db.delete_table(u'roadmap_project')

        # Deleting model 'RoadmapRelease'
        db.delete_table(u'roadmap_roadmaprelease')

        # Deleting model 'FixVersion'
        db.delete_table(u'roadmap_fixversion')

        # Deleting model 'Resolution'
        db.delete_table(u'roadmap_resolution')

        # Deleting model 'StatusStyle'
        db.delete_table(u'roadmap_statusstyle')

        # Deleting model 'Status'
        db.delete_table(u'roadmap_status')

        # Deleting model 'Component'
        db.delete_table(u'roadmap_component')

        # Deleting model 'Label'
        db.delete_table(u'roadmap_label')

        # Deleting model 'Card'
        db.delete_table(u'roadmap_card')

        # Removing M2M table for field components on 'Card'
        db.delete_table(db.shorten_name(u'roadmap_card_components'))

        # Removing M2M table for field implementedby on 'Card'
        db.delete_table(db.shorten_name(u'roadmap_card_implementedby'))

        # Removing M2M table for field dependson on 'Card'
        db.delete_table(db.shorten_name(u'roadmap_card_dependson'))

        # Removing M2M table for field labels on 'Card'
        db.delete_table(db.shorten_name(u'roadmap_card_labels'))


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roadmap.Project']"})
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