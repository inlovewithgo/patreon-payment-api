from flask import Blueprint, jsonify, request
import requests

paid_bp = Blueprint('paid', __name__)

def paid(client):
    @paid_bp.route('/patreon/active')
    def get_active_patreon_members():
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

            active_members = []
            for member in members:
                member_id = member['id']
                comprehensive_info = client.get_comprehensive_member_info(member_id)
                if comprehensive_info['member_details'].get('patron_status') == 'active_patron':
                    active_members.append(comprehensive_info)

            return jsonify(active_members)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return paid_bp


def paid_api():
    return None