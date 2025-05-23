from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from core import consts
from core.utils import (
    generate_crawl_result_file_path,
    generate_crawl_result_attachment_path,
    generate_crawl_request_sitemap_path,
    search_result_file_path,
)


class CrawlRequest(BaseModel):
    team = models.ForeignKey(
        "user.Team",
        on_delete=models.CASCADE,
        verbose_name=_("team"),
        related_name="crawl_requests",
    )
    url = models.URLField(_("url"), max_length=255)
    status = models.CharField(
        _("status"),
        max_length=255,
        choices=consts.CRAWL_STATUS_CHOICES,
        default=consts.CRAWL_STATUS_NEW,
    )
    options = models.JSONField(_("options"), default=dict)
    duration = models.DurationField(_("duration"), null=True)
    sitemap = models.FileField(
        _("sitemap"),
        max_length=255,
        upload_to=generate_crawl_request_sitemap_path,
        null=True,
        blank=True,
    )

    def number_of_documents(self):
        return self.results.count()

    class Meta:
        verbose_name = _("Crawl Request")
        verbose_name_plural = _("Crawl Requests")


class CrawlResult(BaseModel):
    request = models.ForeignKey(
        CrawlRequest,
        on_delete=models.CASCADE,
        related_name="results",
    )
    url = models.URLField(_("url"), max_length=2048)
    result = models.FileField(
        _("result"),
        upload_to=generate_crawl_result_file_path,
    )

    class Meta:
        verbose_name = _("Crawl Result")
        verbose_name_plural = _("Crawl Results")


class CrawlResultAttachment(BaseModel):
    crawl_result = models.ForeignKey(
        CrawlResult,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    attachment_type = models.CharField(
        _("attachment type"),
        max_length=255,
        choices=consts.CRAWL_RESULT_ATTACHMENT_TYPE_CHOICES,
    )
    attachment = models.FileField(
        _("attachment"), max_length=511, upload_to=generate_crawl_result_attachment_path
    )

    class Meta:
        verbose_name = _("Crawl Result Attachment")
        verbose_name_plural = _("Crawl Result Attachments")

    def __str__(self):
        return self.attachment.name

    @property
    def filename(self):
        return self.attachment.name.split("/")[-1]


class SearchRequest(BaseModel):
    team = models.ForeignKey(
        "user.Team",
        on_delete=models.CASCADE,
        verbose_name=_("team"),
        related_name="search_requests",
    )
    query = models.CharField(_("query"), max_length=255)
    search_options = models.JSONField(_("search options"), default=dict)
    result_limit = models.PositiveIntegerField(_("result limit"), default=5)
    duration = models.DurationField(_("duration"), null=True)
    status = models.CharField(
        _("status"),
        max_length=255,
        choices=consts.CRAWL_STATUS_CHOICES,
        default=consts.CRAWL_STATUS_NEW,
    )
    result = models.FileField(
        _("result"),
        max_length=255,
        upload_to=search_result_file_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.query

    class Meta:
        verbose_name = _("Search Request")
        verbose_name_plural = _("Search Requests")
