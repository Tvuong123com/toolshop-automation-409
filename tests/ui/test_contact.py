"""Sprint 2 & 3 - Contact form attachment tests."""
import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage

pytestmark = pytest.mark.ui


def test_contact_empty_attachment_submits_successfully(page, tmp_path):
    """Goal: verify submitting the contact form with a valid 0-byte file attachment.
    Precondition: contact page is reachable and a temporary empty text file exists.
    Expected: success alert 'Thanks for your message!' is displayed."""
    attachment = tmp_path / "note.txt"
    attachment.write_bytes(b"")
    contact = (
        ContactPage(page)
        .open()
        .fill_form("QA", "Bot", "qa-bot@example.com", "webmaster", "A" * 60)
        .attach(str(attachment))
        .submit()
    )
    expect(contact.success).to_contain_text("Thanks for your message!")


def test_contact_non_empty_attachment_shows_error(page, tmp_path):
    """Goal: verify Toolshop rejects a non-empty file attachment on the contact form.
    Precondition: contact page is reachable and a non-empty text file exists.
    Expected: attachment validation error displays 'File should be empty.'."""
    attachment = tmp_path / "non_empty.txt"
    attachment.write_text("hello toolshop", encoding="utf-8")
    contact = (
        ContactPage(page)
        .open()
        .fill_form("QA", "Bot", "qa-bot@example.com", "webmaster", "A" * 60)
        .attach(str(attachment))
        .submit()
    )
    expect(contact.attachment_error).to_contain_text("File should be empty.")
