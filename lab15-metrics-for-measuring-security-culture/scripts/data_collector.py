import sqlite3
import pandas as pd
from datetime import datetime, timedelta


class SecurityCultureDataCollector:
    """Collect security culture metrics from database."""

    def __init__(self, db_path='data/security_culture.db'):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def collect_training_metrics(self, days_back=30):
        """
        Collect training completion and score data.

        Args:
            days_back: Number of days to look back

        Returns:
            DataFrame with training metrics
        """
        since = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        conn = self._connect()

        query = """
            SELECT
                st.employee_id,
                e.department,
                e.role,
                st.training_type,
                st.completion_date,
                st.score
            FROM security_training st
            JOIN employees e ON st.employee_id = e.employee_id
            WHERE st.completion_date >= ?
        """
        df = pd.read_sql_query(query, conn, params=(since,))
        conn.close()

        if not df.empty:
            df["completion_date"] = pd.to_datetime(df["completion_date"], errors="coerce")

        return df

    def collect_phishing_metrics(self, days_back=30):
        """
        Collect phishing simulation results.

        Includes click rates and report rates joined with department.
        """
        since = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        conn = self._connect()

        query = """
            SELECT
                ps.employee_id,
                e.department,
                ps.simulation_date,
                ps.clicked_link,
                ps.reported_email
            FROM phishing_simulations ps
            JOIN employees e ON ps.employee_id = e.employee_id
            WHERE ps.simulation_date >= ?
        """
        df = pd.read_sql_query(query, conn, params=(since,))
        conn.close()

        if not df.empty:
            df["simulation_date"] = pd.to_datetime(df["simulation_date"], errors="coerce")
            df["clicked_link"] = pd.to_numeric(df["clicked_link"], errors="coerce").fillna(0).astype(int)
            df["reported_email"] = pd.to_numeric(df["reported_email"], errors="coerce").fillna(0).astype(int)

        return df

    def collect_incident_metrics(self, days_back=30):
        """
        Collect security incident data.

        Includes incident type and severity.
        """
        since = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        conn = self._connect()

        query = """
            SELECT
                si.employee_id,
                e.department,
                si.incident_date,
                si.incident_type,
                si.severity
            FROM security_incidents si
            LEFT JOIN employees e ON si.employee_id = e.employee_id
            WHERE si.incident_date >= ?
        """
        df = pd.read_sql_query(query, conn, params=(since,))
        conn.close()

        if not df.empty:
            df["incident_date"] = pd.to_datetime(df["incident_date"], errors="coerce")

        return df

    def collect_survey_metrics(self, days_back=30):
        """
        Collect security awareness survey data.

        Groups can be done in analyzer; here we return raw joined data.
        """
        since = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        conn = self._connect()

        query = """
            SELECT
                ss.employee_id,
                e.department,
                ss.survey_date,
                ss.awareness_score,
                ss.behavior_score
            FROM security_surveys ss
            JOIN employees e ON ss.employee_id = e.employee_id
            WHERE ss.survey_date >= ?
        """
        df = pd.read_sql_query(query, conn, params=(since,))
        conn.close()

        if not df.empty:
            df["survey_date"] = pd.to_datetime(df["survey_date"], errors="coerce")
            df["awareness_score"] = pd.to_numeric(df["awareness_score"], errors="coerce").fillna(0).astype(int)
            df["behavior_score"] = pd.to_numeric(df["behavior_score"], errors="coerce").fillna(0).astype(int)

        return df
