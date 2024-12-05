from flask import Blueprint, jsonify, request
import requests

from main import client, app

patreon_api = Blueprint('patreon', __name__)

@patreon_api.route('/patreon')
def get_patreon_members():
    try:
        url = f"{client.BASE_URL}/campaigns"
        response = requests.get(url, headers=client.headers)
        campaigns = response.json().get('data', [])

        if not campaigns:
            return jsonify({"error": "No campaigns found"}), 404

        campaign_id = campaigns[0]['id']

        members_url = f"{client.BASE_URL}/campaigns/{campaign_id}/members"
        members_response = requests.get(
            members_url,
            headers=client.headers,
            params={'page[count]': 10}
        )
        members = members_response.json().get('data', [])

        comprehensive_members = []
        for member in members:
            member_id = member['id']
            comprehensive_info = client.get_comprehensive_member_info(member_id)
            comprehensive_members.append(comprehensive_info)

        return jsonify(comprehensive_members)

    except Exception as e:
        return jsonify({"error": str(e)}), 500