#!/usr/bin/env python3
"""
ROI and cost-benefit analysis for training programs
"""


def calculate_training_roi(
    incidents_before,
    incidents_after,
    num_participants,
    incident_cost=10000,
    cost_per_participant=500,
):
    """
    Calculate return on investment (ROI) for a training program.

    Parameters:
        incidents_before (float): Total incidents before training
        incidents_after (float): Total incidents after training
        num_participants (int): Number of training participants
        incident_cost (float): Estimated cost per incident
        cost_per_participant (float): Training cost per participant

    Returns:
        dict: ROI and cost analysis results
    """

    # Calculate total training cost
    total_training_cost = float(num_participants) * float(cost_per_participant)

    # Calculate incidents prevented
    incidents_prevented = float(incidents_before) - float(incidents_after)
    if incidents_prevented < 0:
        incidents_prevented = 0.0

    # Calculate cost savings
    cost_savings = incidents_prevented * float(incident_cost)

    # Compute ROI percentage
    if total_training_cost == 0:
        roi_percent = 0.0
    else:
        roi_percent = ((cost_savings - total_training_cost) / total_training_cost) * 100.0

    return {
        "num_participants": int(num_participants),
        "incident_cost": float(incident_cost),
        "cost_per_participant": float(cost_per_participant),
        "total_training_cost": float(total_training_cost),
        "incidents_before": float(incidents_before),
        "incidents_after": float(incidents_after),
        "incidents_prevented": float(incidents_prevented),
        "cost_savings": float(cost_savings),
        "roi_percent": float(roi_percent),
    }


def calculate_payback_period(cost_savings_per_month, total_training_cost):
    """
    Calculate payback period in months.

    Parameters:
        cost_savings_per_month (float): Estimated monthly savings
        total_training_cost (float): Total investment cost

    Returns:
        float: Payback period in months
    """

    savings = float(cost_savings_per_month)
    cost = float(total_training_cost)

    if savings <= 0:
        return float("inf")

    return cost / savings
