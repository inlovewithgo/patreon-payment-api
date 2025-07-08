from flask import Blueprint, jsonify, request
import requests
from collections import defaultdict

tier_bp = Blueprint('tier', __name__)

def tier_analytics(client):
    @tier_bp.route('/patreon/tier_analytics')
    def get_tier_analytics():
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

            tier_stats = defaultdict(lambda: {
                'patron_count': 0,
                'total_revenue_cents': 0,
                'active_patrons': 0,
                'inactive_patrons': 0
            })

            for member in members:
                member_id = member['id']
                info = client.get_comprehensive_member_info(member_id)
                
                for tier in info.get('tiers', []):
                    tier_name = tier.get('title', 'No Tier')
                    amount = info['member_details'].get('currently_entitled_amount_cents', 0)
                    
                    tier_stats[tier_name]['patron_count'] += 1
                    tier_stats[tier_name]['total_revenue_cents'] += amount
                    
                    if info['member_details'].get('patron_status') == 'active_patron':
                        tier_stats[tier_name]['active_patrons'] += 1
                    else:
                        tier_stats[tier_name]['inactive_patrons'] += 1

            analytics = {}
            for tier_name, stats in tier_stats.items():
                analytics[tier_name] = {
                    'patron_count': stats['patron_count'],
                    'monthly_revenue_dollars': stats['total_revenue_cents'] / 100,
                    'active_patrons': stats['active_patrons'],
                    'inactive_patrons': stats['inactive_patrons'],
                    'retention_rate': f"{(stats['active_patrons'] / stats['patron_count'] * 100):.2f}%" if stats['patron_count'] > 0 else "0%"
                }

            return jsonify(analytics)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return tier_bp

def tier_api():
    return None
