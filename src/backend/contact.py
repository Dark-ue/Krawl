from backend.client import supabase


class Contact_imp:
    def __init__(self, userid):
        self.uid = userid

    def ip_back(self):

        print(f"DEBUG: Querying Supabase for username -> '{self.uid}'")
        response = (
            supabase.table('user_status')
            .select('ip_address')
            .eq('username', self.uid)
            .execute()
        )

        if response.data and isinstance(response.data, list) and len(response.data) > 0:
            row = response.data[0]
            if isinstance(row, dict):
                return row.get('ip_address')

        return None

