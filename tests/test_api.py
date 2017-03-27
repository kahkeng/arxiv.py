# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os
import pkg_resources

import httpretty
import pytest
import mock

import arxiv
from arxiv.api import Client
from arxiv.config import API_BASE_URL, PDF_BASE_URL


@pytest.mark.httpretty
def test_fetch_one_id(runner):
    body = pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'id_list=1111.2011v2.xml'))
    httpretty.register_uri(httpretty.POST, API_BASE_URL, body=body)

    client = Client()
    orig_post = arxiv.api.post
    with mock.patch('arxiv.api.post') as mock_post:
        mock_post.side_effect = orig_post
        result = client.fetch(['1111.2011v2'])
        assert mock_post.call_count == 1
        assert result['entries'][0]['id'] == 'http://arxiv.org/abs/1111.2011v2'

        # Test that we cached the result
        result = client.fetch(['1111.2011v2'])
        assert mock_post.call_count == 1
        assert result['entries'][0]['id'] == 'http://arxiv.org/abs/1111.2011v2'
