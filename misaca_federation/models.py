# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import AbstractBaseUser, _user_has_perm
from django.contrib.auth.base_user import BaseUserManager
from django.urls import reverse

class AccountDomainBlock(models.Model):
    domain = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey('Account', models.DO_NOTHING, blank=True, null=True, related_name='+')
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'account_domain_blocks'
        unique_together = (('account', 'domain'),)


class AccountModerationNote(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    account = models.ForeignKey('Account', models.DO_NOTHING, related_name='+')
    target_account = models.ForeignKey('Account', models.DO_NOTHING, related_name='+')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'account_moderation_notes'


class Account(models.Model):
    username = models.TextField(unique=True)
    domain = models.TextField(blank=True, null=True)
    secret = models.TextField()
    private_key = models.TextField(blank=True, null=True)
    public_key = models.TextField()
    remote_url = models.TextField()
    salmon_url = models.TextField()
    hub_url = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    note = models.TextField()
    display_name = models.TextField()
    uri = models.TextField()
    url = models.TextField(blank=True, null=True)
    avatar_file_name = models.TextField(blank=True, null=True)
    avatar_content_type = models.TextField(blank=True, null=True)
    avatar_file_size = models.IntegerField(blank=True, null=True)
    avatar_updated_at = models.DateTimeField(blank=True, null=True)
    header_file_name = models.TextField(blank=True, null=True)
    header_content_type = models.TextField(blank=True, null=True)
    header_file_size = models.IntegerField(blank=True, null=True)
    header_updated_at = models.DateTimeField(blank=True, null=True)
    avatar_remote_url = models.TextField(blank=True, null=True)
    subscription_expires_at = models.DateTimeField(blank=True, null=True)
    silenced = models.BooleanField()
    suspended = models.BooleanField()
    locked = models.BooleanField()
    header_remote_url = models.TextField()
    statuses_count = models.IntegerField()
    followers_count = models.IntegerField()
    following_count = models.IntegerField()
    last_webfingered_at = models.DateTimeField(blank=True, null=True)
    inbox_url = models.TextField()
    outbox_url = models.TextField()
    shared_inbox_url = models.TextField()
    followers_url = models.TextField()
    protocol = models.IntegerField()
    id = models.BigAutoField(primary_key=True)
    memorial = models.BooleanField()
    moved_to_account = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='+')
    featured_collection_url = models.TextField(blank=True, null=True)
    fields = JSONField(blank=True, null=True)  # This field type is a guess.
    actor_type = models.TextField(blank=True, null=True)

    def acct(self):
        if self.is_local():
            return self.username
        else:
            return "%s@%s" % (self.username, self.domain)

    def get_avatar_url(self):
        if self.is_local():
            return self.avatar_file_name
        else:
            return self.avatar_remote_url

    def is_local(self):
        return self.domain == None

    def is_bot(self):
        return self.actor_type in ['Application', 'Service']

    def __str__(self):
        if self.domain != None:
            return '%s@%s' % (self.username, self.domain)
        else:
            return self.username

    class Meta:
        db_table = 'accounts'
        unique_together = (('username', 'domain'),)


class AdminActionLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True, related_name='+')
    action = models.TextField()
    target_type = models.TextField(blank=True, null=True)
    target_id = models.BigIntegerField(blank=True, null=True)
    recorded_changes = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'admin_action_logs'


class ArInternalMetadata(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'ar_internal_metadata'


class Backup(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, related_name='+')
    dump_file_name = models.TextField(blank=True, null=True)
    dump_content_type = models.TextField(blank=True, null=True)
    dump_file_size = models.IntegerField(blank=True, null=True)
    dump_updated_at = models.DateTimeField(blank=True, null=True)
    processed = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'backups'


class Block(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    id = models.BigAutoField(primary_key=True)
    target_account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    uri = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'blocks'
        unique_together = (('account', 'target_account'),)


class ConversationMute(models.Model):
    conversation = models.ForeignKey('Conversation', models.DO_NOTHING, related_name='+')
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'conversation_mutes'
        unique_together = (('account', 'conversation'),)


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    uri = models.CharField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'conversations'


class CustomEmoji(models.Model):
    id = models.BigAutoField(primary_key=True)
    shortcode = models.TextField()
    domain = models.TextField(blank=True, null=True)
    image_file_name = models.TextField(blank=True, null=True)
    image_content_type = models.TextField(blank=True, null=True)
    image_file_size = models.IntegerField(blank=True, null=True)
    image_updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    disabled = models.BooleanField()
    uri = models.TextField(blank=True, null=True)
    image_remote_url = models.TextField(blank=True, null=True)
    visible_in_picker = models.BooleanField()

    class Meta:
        db_table = 'custom_emojis'
        unique_together = (('shortcode', 'domain'),)


class DeprecatedPreviewCard(models.Model):
    status = models.OneToOneField('Status', models.DO_NOTHING, blank=True, null=True, related_name='+')
    url = models.TextField()
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_file_name = models.TextField(blank=True, null=True)
    image_content_type = models.TextField(blank=True, null=True)
    image_file_size = models.IntegerField(blank=True, null=True)
    image_updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.IntegerField()
    html = models.TextField()
    author_name = models.TextField()
    author_url = models.TextField()
    provider_name = models.TextField()
    provider_url = models.TextField()
    width = models.IntegerField()
    height = models.IntegerField()
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'deprecated_preview_cards'


class DomainBlock(models.Model):
    domain = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    severity = models.IntegerField(blank=True, null=True)
    reject_media = models.BooleanField()
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'domain_blocks'


class EmailDomainBlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    domain = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'email_domain_blocks'


class Favourite(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    id = models.BigAutoField(primary_key=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, related_name='+')

    class Meta:
        db_table = 'favourites'
        unique_together = (('account', 'status'),)


class FollowRequest(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    id = models.BigAutoField(primary_key=True)
    target_account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    show_reblogs = models.BooleanField()
    uri = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'follow_requests'
        unique_together = (('account', 'target_account'),)


class Follow(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    id = models.BigAutoField(primary_key=True)
    target_account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    show_reblogs = models.BooleanField()
    uri = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'follows'
        unique_together = (('account', 'target_account'),)


class Identity(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, related_name='identities')
    provider = models.TextField()
    uid = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'identities'


class Import(models.Model):
    type = models.IntegerField()
    approved = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    data_file_name = models.TextField(blank=True, null=True)
    data_content_type = models.TextField(blank=True, null=True)
    data_file_size = models.IntegerField(blank=True, null=True)
    data_updated_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'imports'


class Invite(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='+')
    code = models.CharField(unique=True, max_length=255)
    expires_at = models.DateTimeField(blank=True, null=True)
    max_uses = models.IntegerField(blank=True, null=True)
    uses = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'invites'


class ListAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    list = models.ForeignKey('List', models.DO_NOTHING, related_name='+')
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    follow = models.ForeignKey(Follow, models.DO_NOTHING, related_name='+')

    class Meta:
        db_table = 'list_accounts'
        unique_together = (('account', 'list'),)


class List(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    title = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'lists'


class MediaAttachment(models.Model):
    status = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True, related_name='attachments')
    file_file_name = models.TextField(blank=True, null=True)
    file_content_type = models.TextField(blank=True, null=True)
    file_file_size = models.IntegerField(blank=True, null=True)
    file_updated_at = models.DateTimeField(blank=True, null=True)
    remote_url = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    shortcode = models.CharField(unique=True, max_length=255, blank=True, null=True)
    type = models.IntegerField()
    file_meta = models.TextField(blank=True, null=True)  # This field type is a guess.
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True, related_name='+')
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'media_attachments'


class Mention(models.Model):
    status = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True, related_name='mentions')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True, related_name='+')
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'mentions'
        unique_together = (('account', 'status'),)


class Mute(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hide_notifications = models.BooleanField()
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='mutes')
    id = models.BigAutoField(primary_key=True)
    target_account = models.ForeignKey(Account, models.DO_NOTHING, related_name='muted_by')

    class Meta:
        db_table = 'mutes'
        unique_together = (('account', 'target_account'),)


class Notification(models.Model):
    activity_id = models.BigIntegerField()
    activity_type = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='notifications')
    from_account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'notifications'
        unique_together = (('account', 'activity_id', 'activity_type'),)


class OauthAccessGrant(models.Model):
    token = models.CharField(unique=True, max_length=255)
    expires_in = models.IntegerField()
    redirect_uri = models.TextField()
    created_at = models.DateTimeField()
    revoked_at = models.DateTimeField(blank=True, null=True)
    scopes = models.TextField(blank=True, null=True)
    application = models.ForeignKey('OauthApplication', models.DO_NOTHING, related_name='+')
    id = models.BigAutoField(primary_key=True)
    resource_owner = models.ForeignKey('User', models.DO_NOTHING, related_name='+')

    class Meta:
        db_table = 'oauth_access_grants'


class OauthAccessToken(models.Model):
    token = models.CharField(unique=True, max_length=255)
    refresh_token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    expires_in = models.IntegerField(blank=True, null=True)
    revoked_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    scopes = models.TextField(blank=True, null=True)
    application = models.ForeignKey('OauthApplication', models.DO_NOTHING, blank=True, null=True, related_name='+')
    id = models.BigAutoField(primary_key=True)
    resource_owner = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, related_name='+')

    class Meta:
        db_table = 'oauth_access_tokens'


class OauthApplication(models.Model):
    name = models.TextField()
    uid = models.CharField(unique=True, max_length=255)
    secret = models.TextField()
    redirect_uri = models.TextField()
    scopes = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    superapp = models.BooleanField()
    website = models.TextField(blank=True, null=True)
    owner_type = models.TextField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, related_name='+')

    class Meta:
        db_table = 'oauth_applications'


class PreviewCard(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(unique=True, max_length=255)
    title = models.TextField()
    description = models.TextField()
    image_file_name = models.TextField(blank=True, null=True)
    image_content_type = models.TextField(blank=True, null=True)
    image_file_size = models.IntegerField(blank=True, null=True)
    image_updated_at = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField()
    html = models.TextField()
    author_name = models.TextField()
    author_url = models.TextField()
    provider_name = models.TextField()
    provider_url = models.TextField()
    width = models.IntegerField()
    height = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    embed_url = models.TextField()

    class Meta:
        db_table = 'preview_cards'


class PreviewCardStatus(models.Model):
    preview_card_id = models.BigIntegerField()
    status_id = models.BigIntegerField()

    class Meta:
        db_table = 'preview_cards_statuses'


class ReportNote(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    report = models.ForeignKey('Report', models.DO_NOTHING, related_name='report_notes')
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'report_notes'


class Report(models.Model):
    status_ids = ArrayField(models.IntegerField())  # This field type is a guess.
    comment = models.TextField()
    action_taken = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    action_taken_by_account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True, related_name='+')
    id = models.BigAutoField(primary_key=True)
    target_account = models.ForeignKey(Account, models.DO_NOTHING, related_name='reported')
    assigned_account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True, related_name='+')

    class Meta:
        db_table = 'reports'

class SessionActivation(models.Model):
    id = models.BigAutoField(primary_key=True)
    session_id = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user_agent = models.TextField()
    ip = models.GenericIPAddressField(blank=True, null=True)
    access_token = models.ForeignKey(OauthAccessToken, models.DO_NOTHING, blank=True, null=True, related_name='+')
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='+')
    web_push_subscription_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'session_activations'


class Setting(models.Model):
    var = models.TextField()
    value = models.TextField(blank=True, null=True)
    thing_type = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    thing_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'settings'
        unique_together = (('thing_type', 'thing_id', 'var'),)


class SiteUpload(models.Model):
    id = models.BigAutoField(primary_key=True)
    var = models.CharField(unique=True, max_length=255)
    file_file_name = models.TextField(blank=True, null=True)
    file_content_type = models.TextField(blank=True, null=True)
    file_file_size = models.IntegerField(blank=True, null=True)
    file_updated_at = models.DateTimeField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'site_uploads'


class StatusPins(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='pinned')
    status = models.ForeignKey('Status', models.DO_NOTHING, related_name='is_pinned')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'status_pins'
        unique_together = (('account', 'status'),)


class Status(models.Model):
    id = models.BigIntegerField(primary_key=True)
    uri = models.CharField(unique=True, max_length=255, blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    in_reply_to = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='replies')
    reblog_of = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='reblogs')
    url = models.TextField(blank=True, null=True)
    sensitive = models.BooleanField()
    visibility = models.IntegerField()
    spoiler_text = models.TextField()
    reply = models.BooleanField()
    favourites_count = models.IntegerField()
    reblogs_count = models.IntegerField()
    language = models.TextField(blank=True, null=True)
    conversation_id = models.BigIntegerField(blank=True, null=True)
    local = models.NullBooleanField()
    account = models.ForeignKey(Account, models.DO_NOTHING, related_name='statuses')
    application_id = models.BigIntegerField(blank=True, null=True)
    in_reply_to_account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True, related_name='+')
    tags = models.ManyToManyField(
        'Tag',
        through='StatusTag',
        through_fields=('status', 'tag')
    )

    def get_visibility(self):
        VISIBILITY_CHOICES = (
            'public',
            'unlisted',
            'private',
            'direct',
        )
        return VISIBILITY_CHOICES[self.visibility]

    def __str__(self):
        return '%s: %s' % (self.account, self.text)
    class Meta:
        db_table = 'statuses'
        verbose_name_plural = 'statuses'


class StatusTag(models.Model):
    status = models.ForeignKey(Status, models.DO_NOTHING, related_name='+')
    tag = models.ForeignKey('Tag', models.DO_NOTHING, related_name='+')

    class Meta:
        db_table = 'statuses_tags'
        unique_together = (('tag', 'status'),)


class StreamEntry(models.Model):
    activity_id = models.BigIntegerField(blank=True, null=True)
    activity_type = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    hidden = models.BooleanField()
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'stream_entries'


class Subscription(models.Model):
    callback_url = models.TextField()
    secret = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    confirmed = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    last_successful_delivery_at = models.DateTimeField(blank=True, null=True)
    domain = models.TextField(blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'subscriptions'
        unique_together = (('account', 'callback_url'),)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'tags'

class User(Account):
    email = models.CharField(unique=True, max_length=255)
    encrypted_password = models.TextField()
    reset_password_token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    remember_created_at = models.DateTimeField(blank=True, null=True)
    sign_in_count = models.IntegerField()
    current_sign_in_at = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True, db_column='last_sign_in_at')
    current_sign_in_ip = models.GenericIPAddressField(blank=True, null=True)
    last_sign_in_ip = models.GenericIPAddressField(blank=True, null=True)
    admin = models.BooleanField()
    confirmation_token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmation_sent_at = models.DateTimeField(blank=True, null=True)
    unconfirmed_email = models.TextField(blank=True, null=True)
    locale = models.TextField(blank=True, null=True)
    encrypted_otp_secret = models.TextField(blank=True, null=True)
    encrypted_otp_secret_iv = models.TextField(blank=True, null=True)
    encrypted_otp_secret_salt = models.TextField(blank=True, null=True)
    consumed_timestep = models.IntegerField(blank=True, null=True)
    otp_required_for_login = models.BooleanField()
    last_emailed_at = models.DateTimeField(blank=True, null=True)
    otp_backup_codes = ArrayField(models.TextField(blank=True, null=True))  # This field type is a guess.
    filtered_languages = ArrayField(models.TextField())  # This field type is a guess.
    account = models.OneToOneField(Account, models.DO_NOTHING)
    user_id = models.BigAutoField(primary_key=True, db_column="id")
    disabled = models.BooleanField()
    moderator = models.BooleanField()
    invite = models.ForeignKey(Invite, models.DO_NOTHING, blank=True, null=True, related_name='+')
    remember_token = models.TextField(blank=True, null=True)
    
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE,
        parent_link=True,
    )

    # Django compatibility
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    objects = BaseUserManager()

    def get_full_name(self):
        return self.display_name

    @property
    def is_staff(self):
        return self.is_superuser or self.is_admin
    @property
    def is_admin(self):
        return self.moderator
    @property
    def is_superuser(self):
        return self.admin
    @property
    def is_anonymous(self):
        return False
    @property
    def is_authenticated(self):
        return True
    @property
    def password(self):
        return 'bcrypt$'+self.encrypted_password

    @property
    def is_active(self):
        return not self.suspended

    @property
    def date_joined(self):
        return self.created_at
    @property
    def last_signed_in_at(self):
        return self.last_login
    
    @last_signed_in_at.setter
    def last_signed_in_at(self, value):
        self.last_login = value

    def check_password(self, raw_password):
        import bcrypt
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.encrypted_password.encode('utf-8'))
    
    def set_password(self, raw_password):
        import bcrypt
        return bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())

    def has_perm(self, perm, obj = None):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)
    
    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, package_name):
        if package_name == 'auth':
            return self.is_staff
        else:
            return True

    class Meta:
        db_table = 'users'

class WebPushSubscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    endpoint = models.TextField()
    key_p256dh = models.TextField()
    key_auth = models.TextField()
    data = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    access_token = models.ForeignKey(OauthAccessToken, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'web_push_subscriptions'


class WebSetting(models.Model):
    data = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, models.DO_NOTHING)

    class Meta:
        db_table = 'web_settings'
