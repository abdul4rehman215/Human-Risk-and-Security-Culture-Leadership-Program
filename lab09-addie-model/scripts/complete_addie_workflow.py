#!/usr/bin/env python3
"""
Complete ADDIE Workflow Integration
Workflow orchestration with persistence
"""

import os
import sys
import json
from datetime import datetime

# Ensure scripts directory is in path so imports work
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from addie_framework import ADDIEFramework
from analyze_phase import AnalyzePhase
from design_phase import DesignPhase
from develop_phase import DevelopPhase
from implement_phase import ImplementPhase
from evaluate_phase import EvaluatePhase


class ADDIEWorkflow:
    def __init__(self, project_name: str):
        self.framework = ADDIEFramework(project_name)
        self.phases = {
            "analyze": AnalyzePhase(),
            "design": None,
            "develop": None,
            "implement": ImplementPhase(),
            "evaluate": EvaluatePhase(),
        }

        # Ensure phase folders exist
        for d in ["analyze", "design", "develop", "implement", "evaluate", "reports", "data"]:
            os.makedirs(os.path.join(PROJECT_ROOT, d), exist_ok=True)

    def run_complete_workflow(self):
        """Execute complete ADDIE workflow"""

        # Run analyze phase
        self.framework.update_phase_status("analyze", "in_progress")
        analyzer = self.phases["analyze"]
        analyzer.conduct_needs_assessment()
        analyzer.analyze_learners()
        analyzer.identify_goals()
        analyzer.document_constraints()
        analyze_file = analyzer.generate_analysis_report(output_dir=os.path.join(PROJECT_ROOT, "analyze"))
        self.framework.project_data["phases"]["analyze"]["data"] = analyzer.analysis_data
        self.framework.update_phase_status("analyze", "complete")

        # Pass analysis data to design phase
        self.framework.update_phase_status("design", "in_progress")
        self.phases["design"] = DesignPhase(analysis_data=analyzer.analysis_data)
        designer = self.phases["design"]
        designer.create_learning_objectives()
        designer.design_assessment_strategy()
        designer.design_instructional_strategy()
        designer.create_content_outline()
        designer.design_delivery_method()
        design_json, design_txt = designer.generate_design_document(output_dir=os.path.join(PROJECT_ROOT, "design"))
        self.framework.project_data["phases"]["design"]["data"] = designer.design_data
        self.framework.update_phase_status("design", "complete")

        # Pass design data to develop phase
        self.framework.update_phase_status("develop", "in_progress")
        self.phases["develop"] = DevelopPhase(design_data=designer.design_data)
        developer = self.phases["develop"]
        developer.create_content_materials()
        developer.develop_assessments()
        developer.create_multimedia_resources()
        developer.conduct_quality_assurance()
        develop_json, develop_txt = developer.generate_development_report(output_dir=os.path.join(PROJECT_ROOT, "develop"))
        self.framework.project_data["phases"]["develop"]["data"] = developer.develop_data
        self.framework.update_phase_status("develop", "complete")

        # Execute implement phase
        self.framework.update_phase_status("implement", "in_progress")
        implementer = self.phases["implement"]
        implementer.plan_deployment()
        implementer.track_participants()
        implementer.provide_support()
        implementer.update_completion()
        implement_json, implement_txt = implementer.save_implementation_report(output_dir=os.path.join(PROJECT_ROOT, "implement"))
        self.framework.project_data["phases"]["implement"]["data"] = implementer.implement_data
        self.framework.update_phase_status("implement", "complete")

        # Run evaluate phase
        self.framework.update_phase_status("evaluate", "in_progress")
        evaluator = self.phases["evaluate"]
        evaluator.evaluate_reaction()
        evaluator.evaluate_learning()
        evaluator.evaluate_behavior()
        evaluator.evaluate_results()
        evaluator.generate_recommendations()
        eval_json, eval_txt = evaluator.create_evaluation_report(output_dir=os.path.join(PROJECT_ROOT, "evaluate"))
        self.framework.project_data["phases"]["evaluate"]["data"] = evaluator.evaluation_data
        self.framework.update_phase_status("evaluate", "complete")

        # Generate final project report
        final_report = self.generate_project_report(
            analyze_file=analyze_file,
            design_json=design_json,
            design_txt=design_txt,
            develop_json=develop_json,
            develop_txt=develop_txt,
            implement_json=implement_json,
            implement_txt=implement_txt,
            eval_json=eval_json,
            eval_txt=eval_txt,
        )

        # Save project state
        self.framework.save_project()

        print("\n=== WORKFLOW COMPLETE ===")
        print(f"Final report saved: {final_report}")
        self.framework.display_project_overview()

    def run_phase(self, phase_name: str):
        """Run a specific phase"""

        valid = ["analyze", "design", "develop", "implement", "evaluate"]
        if phase_name not in valid:
            print("Invalid phase name.")
            return

        print(f"\n=== RUNNING PHASE: {phase_name.upper()} ===")
        self.framework.update_phase_status(phase_name, "in_progress")

        if phase_name == "analyze":
            analyzer = self.phases["analyze"]
            analyzer.conduct_needs_assessment()
            analyzer.analyze_learners()
            analyzer.identify_goals()
            analyzer.document_constraints()
            analyzer.generate_analysis_report(output_dir=os.path.join(PROJECT_ROOT, "analyze"))
            self.framework.project_data["phases"]["analyze"]["data"] = analyzer.analysis_data

        elif phase_name == "design":
            analysis_data = self.framework.project_data["phases"]["analyze"]["data"]
            self.phases["design"] = DesignPhase(analysis_data=analysis_data)
            designer = self.phases["design"]
            designer.create_learning_objectives()
            designer.design_assessment_strategy()
            designer.design_instructional_strategy()
            designer.create_content_outline()
            designer.design_delivery_method()
            designer.generate_design_document(output_dir=os.path.join(PROJECT_ROOT, "design"))
            self.framework.project_data["phases"]["design"]["data"] = designer.design_data

        elif phase_name == "develop":
            design_data = self.framework.project_data["phases"]["design"]["data"]
            self.phases["develop"] = DevelopPhase(design_data=design_data)
            developer = self.phases["develop"]
            developer.create_content_materials()
            developer.develop_assessments()
            developer.create_multimedia_resources()
            developer.conduct_quality_assurance()
            developer.generate_development_report(output_dir=os.path.join(PROJECT_ROOT, "develop"))
            self.framework.project_data["phases"]["develop"]["data"] = developer.develop_data

        elif phase_name == "implement":
            implementer = self.phases["implement"]
            implementer.plan_deployment()
            implementer.track_participants()
            implementer.provide_support()
            implementer.update_completion()
            implementer.save_implementation_report(output_dir=os.path.join(PROJECT_ROOT, "implement"))
            self.framework.project_data["phases"]["implement"]["data"] = implementer.implement_data

        elif phase_name == "evaluate":
            evaluator = self.phases["evaluate"]
            evaluator.evaluate_reaction()
            evaluator.evaluate_learning()
            evaluator.evaluate_behavior()
            evaluator.evaluate_results()
            evaluator.generate_recommendations()
            evaluator.create_evaluation_report(output_dir=os.path.join(PROJECT_ROOT, "evaluate"))
            self.framework.project_data["phases"]["evaluate"]["data"] = evaluator.evaluation_data

        self.framework.update_phase_status(phase_name, "complete")
        self.framework.save_project()

        print(f"Phase {phase_name} complete and saved.")

    def generate_project_report(self, **artifact_paths):
        """Generate comprehensive project report"""

        report_dir = os.path.join(PROJECT_ROOT, "reports")
        os.makedirs(report_dir, exist_ok=True)

        report_path = os.path.join(
            report_dir,
            f"final_project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(report_path, "w") as f:
            f.write("=== FINAL ADDIE PROJECT REPORT ===\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            f.write("PROJECT OVERVIEW:\n")
            f.write(json.dumps(self.framework.project_data, indent=4))
            f.write("\n\nARTIFACTS CREATED:\n")
            for k, v in artifact_paths.items():
                f.write(f"- {k}: {v}\n")

            f.write("\n\nNOTES:\n")
            f.write(
                "This report consolidates outputs generated across Analyze, Design, Develop, "
                "Implement, and Evaluate phases.\n"
            )

        return report_path


if __name__ == "__main__":
    workflow = ADDIEWorkflow("Security_Awareness_Training")
    workflow.run_complete_workflow()
