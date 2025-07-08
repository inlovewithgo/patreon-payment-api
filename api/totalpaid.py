from flask import Blueprint, jsonify, request
import requests

total_bp = Blueprint('total', __name__)

def total(client):
    @total_bp.route('/patreon/total_pledges')
    def get_total_pledges():
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
                params={'page[count]': 100}
            )
            members = members_response.json().get('data', [])

            total_cents = 0
            active_count = 0
            pledge_tiers = {}

            for member in members:
                member_id = member['id']
                comprehensive_info = client.get_comprehensive_member_info(member_id)
                
                if comprehensive_info['member_details'].get('patron_status') == 'active_patron':
                    amount = comprehensive_info['member_details'].get('currently_entitled_amount_cents', 0)
                    total_cents += amount
                    active_count += 1
                    
                    for tier in comprehensive_info.get('tiers', []):
                        tier_title = tier.get('title', 'Unknown Tier')
                        pledge_tiers[tier_title] = pledge_tiers.get(tier_title, 0) + 1

            return jsonify({
                "total_pledges_dollars": total_cents / 100,
                "active_patrons": active_count,
                "pledge_tiers_distribution": pledge_tiers,
                "average_pledge": (total_cents / active_count / 100) if active_count > 0 else 0
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return total_bp

def total_api():
    return None
