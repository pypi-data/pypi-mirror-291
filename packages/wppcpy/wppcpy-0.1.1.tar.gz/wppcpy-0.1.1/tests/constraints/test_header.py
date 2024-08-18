import os
import pytest
from wppcpy.constraints.header import (
    PluginName, PluginURI, Description, Version,
    RequiresAtLeast, RequiresPHP, Author, AuthorURI,
    License, LicenseURI, TextDomain, DomainPath,
    Network, UpdateURI, RequiresPlugins
)
@pytest.fixture
def temp_plugin_dir(tmp_path):
    plugin_dir = tmp_path / "test-plugin"
    plugin_dir.mkdir()
    main_file = plugin_dir / "test-plugin.php"
    main_file.write_text("""
    <?php
    /*
     * Plugin Name: Test Plugin
     * Plugin URI: https://example.com
     * Description: A test plugin.
     * Version: 1.0.0
     * Requires at least: 5.0
     * Requires PHP: 7.2
     * Author: John Doe
     * Author URI: https://example.com
     * License: GPLv2
     * License URI: https://www.gnu.org/licenses/gpl-2.0.html
     * Text Domain: test-plugin
     * Domain Path: /languages
     * Network: true
     * Update URI: https://example.com/update
     * Requires Plugins: some-plugin
     */
    """)
    return str(plugin_dir)
def test_plugin_name(temp_plugin_dir):
    constraint = PluginName(temp_plugin_dir)
    assert constraint.validate()

def test_plugin_uri(temp_plugin_dir):
    constraint = PluginURI(temp_plugin_dir)
    assert constraint.validate()

def test_description(temp_plugin_dir):
    constraint = Description(temp_plugin_dir)
    assert constraint.validate()

def test_version(temp_plugin_dir):
    constraint = Version(temp_plugin_dir)
    assert constraint.validate()

def test_requires_at_least(temp_plugin_dir):
    constraint = RequiresAtLeast(temp_plugin_dir)
    assert constraint.validate()

def test_requires_php(temp_plugin_dir):
    constraint = RequiresPHP(temp_plugin_dir)
    assert constraint.validate()

def test_author(temp_plugin_dir):
    constraint = Author(temp_plugin_dir)
    assert constraint.validate()

def test_author_uri(temp_plugin_dir):
    constraint = AuthorURI(temp_plugin_dir)
    assert constraint.validate()

def test_license(temp_plugin_dir):
    constraint = License(temp_plugin_dir)
    assert constraint.validate()

def test_license_uri(temp_plugin_dir):
    constraint = LicenseURI(temp_plugin_dir)
    assert constraint.validate()

def test_text_domain(temp_plugin_dir):
    constraint = TextDomain(temp_plugin_dir)
    assert constraint.validate()

def test_domain_path(temp_plugin_dir):
    constraint = DomainPath(temp_plugin_dir)
    assert constraint.validate()

def test_network(temp_plugin_dir):
    constraint = Network(temp_plugin_dir)
    assert constraint.validate()

def test_update_uri(temp_plugin_dir):
    constraint = UpdateURI(temp_plugin_dir)
    assert constraint.validate()

def test_requires_plugins(temp_plugin_dir):
    constraint = RequiresPlugins(temp_plugin_dir)
    assert constraint.validate()
