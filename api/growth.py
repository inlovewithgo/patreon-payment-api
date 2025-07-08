from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import requests

growth_bp = Blueprint('growth', __name__)

def get_balance(client):
    @get_balance('/api/v1/fetch/balance')

def growth(client):
    @growth_bp.route('/patreon/growth_stats')
    def get_growth_stats():
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

            monthly_stats = {
                'new_patrons': 0,
                'churned_patrons': 0,
                'total_growth': 0
            }

            current_date = datetime.now()
            thirty_days_ago = current_date - timedelta(days=30)

            for member in members:
                member_id = member['id']
                info = client.get_comprehensive_member_info(member_id)
                
                start_date = info['member_details'].get('pledge_relationship_start')
                if start_date:
                    start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    if start_date > thirty_days_ago:
                        monthly_stats['new_patrons'] += 1

                if info['member_details'].get('patron_status') != 'active_patron':
                    last_charge = info['member_details'].get('last_charge_date')
                    if last_charge:
                        last_charge = datetime.fromisoformat(last_charge.replace('Z', '+00:00'))
                        if last_charge > thirty_days_ago:
                            monthly_stats['churned_patrons'] += 1

            monthly_stats['total_growth'] = monthly_stats['new_patrons'] - monthly_stats['churned_patrons']

            return jsonify({
                "last_30_days": monthly_stats,
                "growth_rate": f"{(monthly_stats['total_growth'] / len(members) * 100):.2f}%"
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return growth_bp

def growth_api():
    return None
