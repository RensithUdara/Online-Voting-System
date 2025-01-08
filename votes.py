from database import execute_query

class VotingSystem:
    @staticmethod
    def vote(user_id, party):
        """Cast a vote for a party."""
        # Check if the user has already voted
        result = execute_query(
            "SELECT has_voted FROM users WHERE id = ?",
            (user_id,),
            fetch=True
        )
        if result and result[0][0]:
            return False  # User has already voted

        # Update the vote count for the party
        execute_query(
            "UPDATE votes SET votes = votes + 1 WHERE party = ?",
            (party,)
        )

        # Mark the user as having voted
        execute_query(
            "UPDATE users SET has_voted = TRUE WHERE id = ?",
            (user_id,)
        )
        return True

    @staticmethod
    def get_results():
        """Get the current voting results."""
        return execute_query("SELECT party, votes FROM votes", fetch=True)

    @staticmethod
    def reset_votes():
        """Reset all votes to zero."""
        execute_query("UPDATE votes SET votes = 0")