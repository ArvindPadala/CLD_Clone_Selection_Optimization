import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

class CLDAIAgent:
    """
    AI Agent for CLD Clone Selection Dashboard
    Provides intelligent recommendations, automated analysis, and interactive assistance
    """
    
    def __init__(self):
        self.conversation_history = []
        self.analysis_cache = {}
        self.recommendation_rules = self._load_recommendation_rules()
        
    def _load_recommendation_rules(self) -> Dict:
        """Load AI recommendation rules and thresholds."""
        return {
            "performance_thresholds": {
                "excellent": 0.8,
                "good": 0.6,
                "fair": 0.4,
                "poor": 0.2
            },
            "sensitivity_thresholds": {
                "high": 0.2,
                "medium": 0.1,
                "low": 0.05
            },
            "correlation_thresholds": {
                "high": 0.7,
                "medium": 0.5,
                "low": 0.3
            },
            "data_quality_thresholds": {
                "outlier_threshold": 0.05,  # 5% outliers
                "missing_data_threshold": 0.1,  # 10% missing
                "skewness_threshold": 2.0
            }
        }
    
    def analyze_data_quality(self, df: pd.DataFrame) -> Dict:
        """Analyze data quality and provide AI insights."""
        analysis = {
            "quality_score": 0.0,
            "issues": [],
            "recommendations": [],
            "warnings": [],
            "strengths": []
        }
        
        # Check for required columns
        if "Results" not in df.columns:
            analysis["issues"].append("Missing required 'Results' column")
            return analysis
        
        results = df["Results"].dropna()
        
        # Data completeness
        completeness = len(results) / len(df)
        if completeness < 0.9:
            analysis["issues"].append(f"Low data completeness: {completeness:.1%}")
            analysis["recommendations"].append("Consider cleaning data to remove missing values")
        else:
            analysis["strengths"].append(f"Good data completeness: {completeness:.1%}")
        
        # Outlier detection
        Q1, Q3 = results.quantile([0.25, 0.75])
        IQR = Q3 - Q1
        outliers = results[(results < Q1 - 1.5 * IQR) | (results > Q3 + 1.5 * IQR)]
        outlier_ratio = len(outliers) / len(results)
        
        if outlier_ratio > self.recommendation_rules["data_quality_thresholds"]["outlier_threshold"]:
            analysis["warnings"].append(f"High outlier ratio: {outlier_ratio:.1%}")
            analysis["recommendations"].append("Review outliers for biological relevance")
        else:
            analysis["strengths"].append(f"Low outlier ratio: {outlier_ratio:.1%}")
        
        # Distribution analysis
        skewness = results.skew()
        if abs(skewness) > self.recommendation_rules["data_quality_thresholds"]["skewness_threshold"]:
            analysis["warnings"].append(f"Highly skewed distribution: {skewness:.2f}")
            analysis["recommendations"].append("Consider using KDE instead of lognormal distribution")
        else:
            analysis["strengths"].append(f"Reasonable distribution skewness: {skewness:.2f}")
        
        # Calculate quality score
        analysis["quality_score"] = min(1.0, completeness * (1 - outlier_ratio) * (1 - abs(skewness) / 5))
        
        return analysis
    
    def analyze_simulation_results(self, results: Dict) -> Dict:
        """Analyze simulation results and provide AI insights."""
        analysis = {
            "performance_level": "unknown",
            "key_insights": [],
            "optimization_opportunities": [],
            "recommendations": [],
            "risk_assessments": []
        }
        
        if "probabilities" not in results:
            return analysis
        
        probabilities = results["probabilities"]
        correlations = results["correlations"]
        
        # Performance analysis
        max_prob = max(probabilities)
        min_prob = min(probabilities)
        avg_prob = np.mean(probabilities)
        optimal_corr = correlations[np.argmax(probabilities)]
        
        # Determine performance level
        thresholds = self.recommendation_rules["performance_thresholds"]
        if max_prob >= thresholds["excellent"]:
            analysis["performance_level"] = "excellent"
            analysis["key_insights"].append(f"Outstanding performance: {max_prob:.1%} success rate")
            analysis["recommendations"].append("Current parameters are optimal - consider resource optimization")
        elif max_prob >= thresholds["good"]:
            analysis["performance_level"] = "good"
            analysis["key_insights"].append(f"Good performance: {max_prob:.1%} success rate")
            analysis["optimization_opportunities"].append("Room for improvement through parameter optimization")
        elif max_prob >= thresholds["fair"]:
            analysis["performance_level"] = "fair"
            analysis["key_insights"].append(f"Fair performance: {max_prob:.1%} success rate")
            analysis["optimization_opportunities"].append("Significant optimization opportunities available")
        else:
            analysis["performance_level"] = "poor"
            analysis["key_insights"].append(f"Poor performance: {max_prob:.1%} success rate")
            analysis["risk_assessments"].append("Major parameter review required")
        
        # Correlation analysis
        if optimal_corr > self.recommendation_rules["correlation_thresholds"]["high"]:
            analysis["key_insights"].append(f"High optimal correlation ({optimal_corr:.2f}) - strong assay consistency beneficial")
            analysis["recommendations"].append("Invest in improving assay correlation for better results")
        elif optimal_corr > self.recommendation_rules["correlation_thresholds"]["medium"]:
            analysis["key_insights"].append(f"Moderate optimal correlation ({optimal_corr:.2f}) - reasonable assay consistency")
        else:
            analysis["key_insights"].append(f"Low optimal correlation ({optimal_corr:.2f}) - correlation less critical")
        
        # Improvement potential
        improvement_range = max_prob - min_prob
        if improvement_range > 0.3:
            analysis["optimization_opportunities"].append(f"High improvement potential: {improvement_range:.1%} range")
        elif improvement_range > 0.2:
            analysis["optimization_opportunities"].append(f"Moderate improvement potential: {improvement_range:.1%} range")
        else:
            analysis["key_insights"].append(f"Low improvement potential: {improvement_range:.1%} range")
        
        return analysis
    
    def generate_parameter_recommendations(self, df: pd.DataFrame, current_settings: Dict) -> Dict:
        """Generate intelligent parameter recommendations based on data characteristics."""
        recommendations = {
            "workflow_recommendation": "",
            "step_sizes": {},
            "distribution_method": "",
            "correlation_range": (0.1, 0.9),
            "simulation_settings": {},
            "reasoning": []
        }
        
        # Analyze data characteristics
        results = df["Results"].dropna()
        data_size = len(results)
        skewness = results.skew()
        criteria_columns = [col for col in df.columns if col.lower().startswith("criteria")]
        
        # Workflow recommendation
        if data_size > 2000:
            recommendations["workflow_recommendation"] = "3-step workflow"
            recommendations["reasoning"].append("Large dataset (>2000 clones) - 3-step workflow provides better selection")
        elif data_size > 1000:
            recommendations["workflow_recommendation"] = "2-step workflow"
            recommendations["reasoning"].append("Medium dataset (1000-2000 clones) - 2-step workflow is efficient")
        else:
            recommendations["workflow_recommendation"] = "2-step workflow"
            recommendations["reasoning"].append("Small dataset (<1000 clones) - 2-step workflow recommended")
        
        # Step size recommendations
        if data_size > 2000:
            recommendations["step_sizes"] = {
                "step1_keep": min(192, data_size // 10),
                "step2_keep": min(96, data_size // 20),
                "step3_keep": 6
            }
        elif data_size > 1000:
            recommendations["step_sizes"] = {
                "step1_keep": min(96, data_size // 10),
                "step2_keep": min(48, data_size // 20),
                "step3_keep": 6
            }
        else:
            recommendations["step_sizes"] = {
                "step1_keep": min(48, data_size // 5),
                "step2_keep": min(24, data_size // 10),
                "step3_keep": 6
            }
        
        # Distribution method recommendation
        if abs(skewness) > 2:
            recommendations["distribution_method"] = "kde"
            recommendations["reasoning"].append(f"Highly skewed data (skewness={skewness:.2f}) - KDE recommended")
        else:
            recommendations["distribution_method"] = "lognormal"
            recommendations["reasoning"].append(f"Moderate skewness (skewness={skewness:.2f}) - Lognormal suitable")
        
        # Simulation settings
        if data_size > 2000:
            recommendations["simulation_settings"] = {
                "n_rep": 5000,
                "correlation_step_size": 0.05
            }
        else:
            recommendations["simulation_settings"] = {
                "n_rep": 10000,
                "correlation_step_size": 0.01
            }
        
        # Criteria recommendations
        if criteria_columns:
            recommendations["reasoning"].append(f"Criteria columns detected: {len(criteria_columns)} - consider using filtering")
        
        return recommendations
    
    def analyze_sensitivity_results(self, sensitivity_results: Dict) -> Dict:
        """Analyze sensitivity analysis results and provide AI insights."""
        analysis = {
            "critical_parameters": [],
            "stable_parameters": [],
            "optimization_priorities": [],
            "insights": []
        }
        
        for param_name, data in sensitivity_results.items():
            values = data['values']
            probabilities = data['probabilities']
            
            # Calculate sensitivity
            max_prob = max(probabilities)
            min_prob = min(probabilities)
            sensitivity = max_prob - min_prob
            
            # Categorize parameter sensitivity
            if sensitivity > self.recommendation_rules["sensitivity_thresholds"]["high"]:
                analysis["critical_parameters"].append(param_name)
                analysis["optimization_priorities"].append(f"High priority: {param_name} (sensitivity: {sensitivity:.1%})")
            elif sensitivity > self.recommendation_rules["sensitivity_thresholds"]["medium"]:
                analysis["insights"].append(f"Moderate sensitivity: {param_name} (sensitivity: {sensitivity:.1%})")
            else:
                analysis["stable_parameters"].append(param_name)
                analysis["insights"].append(f"Low sensitivity: {param_name} (sensitivity: {sensitivity:.1%})")
        
        return analysis
    
    def generate_workflow_optimization_plan(self, current_results: Dict, sensitivity_results: Dict) -> Dict:
        """Generate a comprehensive optimization plan based on current results and sensitivity analysis."""
        plan = {
            "immediate_actions": [],
            "short_term_optimizations": [],
            "long_term_considerations": [],
            "expected_improvements": [],
            "risk_mitigation": []
        }
        
        # Analyze current performance
        if "probabilities" in current_results:
            max_prob = max(current_results["probabilities"])
            
            if max_prob < 0.4:
                plan["immediate_actions"].append("Review all workflow parameters - current performance is poor")
                plan["short_term_optimizations"].append("Test different step sizes and correlation ranges")
            elif max_prob < 0.6:
                plan["immediate_actions"].append("Optimize high-sensitivity parameters identified in sensitivity analysis")
                plan["short_term_optimizations"].append("Fine-tune correlation and threshold settings")
            elif max_prob < 0.8:
                plan["short_term_optimizations"].append("Minor parameter adjustments for marginal improvements")
                plan["long_term_considerations"].append("Consider workflow efficiency optimization")
            else:
                plan["long_term_considerations"].append("Focus on resource optimization and workflow efficiency")
        
        # Use sensitivity analysis for specific recommendations
        if sensitivity_results:
            critical_params = []
            for param_name, data in sensitivity_results.items():
                sensitivity = max(data['probabilities']) - min(data['probabilities'])
                if sensitivity > 0.2:
                    critical_params.append(param_name)
            
            if critical_params:
                plan["short_term_optimizations"].append(f"Focus optimization on: {', '.join(critical_params)}")
        
        return plan
    
    def chat_interface(self, user_message: str, context: Dict) -> str:
        """Interactive chat interface for user queries."""
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "context": context
        })
        
        # Simple rule-based responses (can be enhanced with LLM integration)
        user_message_lower = user_message.lower()
        
        if "help" in user_message_lower or "how" in user_message_lower:
            return self._generate_help_response(user_message, context)
        elif "optimize" in user_message_lower or "improve" in user_message_lower:
            return self._generate_optimization_response(context)
        elif "explain" in user_message_lower or "what" in user_message_lower:
            return self._generate_explanation_response(user_message, context)
        elif "recommend" in user_message_lower or "suggest" in user_message_lower:
            return self._generate_recommendation_response(context)
        else:
            return self._generate_general_response(user_message, context)
    
    def _generate_help_response(self, message: str, context: Dict) -> str:
        """Generate help response based on user query."""
        if "correlation" in message.lower():
            return "Correlation measures the relationship between assay steps. Higher correlation means more consistent results between steps. Use sensitivity analysis to find the optimal correlation for your data."
        elif "sensitivity" in message.lower():
            return "Sensitivity analysis shows how much each parameter affects success probability. Focus optimization on high-sensitivity parameters for maximum impact."
        elif "workflow" in message.lower():
            return "2-step workflows are simpler and faster, while 3-step workflows provide more selection stages. Choose based on your data size and resource constraints."
        else:
            return "I can help you with parameter optimization, result interpretation, workflow selection, and data analysis. What specific aspect would you like to know more about?"
    
    def _generate_optimization_response(self, context: Dict) -> str:
        """Generate optimization recommendations."""
        if "probabilities" in context:
            max_prob = max(context["probabilities"])
            if max_prob < 0.4:
                return "Your current performance is poor. I recommend: 1) Review all parameters, 2) Check data quality, 3) Test different correlation ranges, 4) Consider alternative workflows."
            elif max_prob < 0.6:
                return "Good optimization opportunities available. Focus on: 1) High-sensitivity parameters, 2) Correlation optimization, 3) Step size adjustments."
            else:
                return "Performance is good. Consider: 1) Resource optimization, 2) Workflow efficiency improvements, 3) Fine-tuning for marginal gains."
        else:
            return "Run a simulation first to get optimization recommendations based on your specific data and parameters."
    
    def _generate_explanation_response(self, message: str, context: Dict) -> str:
        """Generate explanation response."""
        if "success probability" in message.lower():
            return "Success probability is the likelihood that ALL final selected clones are in the top X% of performers. Higher values indicate better selection quality."
        elif "correlation" in message.lower():
            return "Correlation between 0-1 measures assay consistency. 0.7+ means strong consistency, 0.5 means moderate, <0.3 means weak consistency."
        else:
            return "I can explain any aspect of the simulation, results, or parameters. What would you like me to clarify?"
    
    def _generate_recommendation_response(self, context: Dict) -> str:
        """Generate parameter recommendations."""
        if "df" in context:
            df = context["df"]
            recommendations = self.generate_parameter_recommendations(df, {})
            return f"Based on your data ({len(df)} clones), I recommend: {recommendations['workflow_recommendation']}, {recommendations['distribution_method']} distribution, and step sizes of {recommendations['step_sizes']}."
        else:
            return "Upload your data first to get personalized recommendations based on your specific dataset characteristics."
    
    def _generate_general_response(self, message: str, context: Dict) -> str:
        """Generate general response for unrecognized queries."""
        return "I'm here to help with your CLD clone selection analysis. You can ask me about: parameter optimization, result interpretation, workflow recommendations, data analysis, or any other aspect of the dashboard. What would you like to know?"
    
    def export_ai_analysis(self) -> str:
        """Export AI analysis as a comprehensive report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "conversation_history": self.conversation_history,
            "analysis_cache": self.analysis_cache,
            "summary": "AI Agent Analysis Report"
        }
        return json.dumps(report, indent=2)

def create_ai_agent_interface():
    """Create the AI agent interface in Streamlit."""
    st.markdown("## 🤖 AI Agent Assistant")
    
    # Initialize AI agent
    if "ai_agent" not in st.session_state:
        st.session_state.ai_agent = CLDAIAgent()
    
    ai_agent = st.session_state.ai_agent
    
    # Chat interface
    st.markdown("### 💬 Chat with AI Assistant")
    
    # Chat input
    user_input = st.text_input("Ask me anything about your CLD analysis:", key="ai_chat_input")
    
    if user_input:
        # Get current context
        context = {}
        if "df" in st.session_state:
            context["df"] = st.session_state.df
        if "probabilities" in st.session_state:
            context["probabilities"] = st.session_state.probabilities
        if "sensitivity_results" in st.session_state:
            context["sensitivity_results"] = st.session_state.sensitivity_results
        
        # Generate response
        response = ai_agent.chat_interface(user_input, context)
        
        # Display conversation
        st.markdown("**AI Assistant:** " + response)
    
    # Quick action buttons
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Analyze Data Quality"):
            if "df" in st.session_state:
                analysis = ai_agent.analyze_data_quality(st.session_state.df)
                st.session_state.data_quality_analysis = analysis
                st.success("Data quality analysis complete!")
            else:
                st.warning("Please upload data first")
    
    with col2:
        if st.button("🎯 Get Recommendations"):
            if "df" in st.session_state:
                recommendations = ai_agent.generate_parameter_recommendations(
                    st.session_state.df, {}
                )
                st.session_state.ai_recommendations = recommendations
                st.success("AI recommendations generated!")
            else:
                st.warning("Please upload data first")
    
    with col3:
        if st.button("📈 Analyze Results"):
            if "probabilities" in st.session_state:
                analysis = ai_agent.analyze_simulation_results(st.session_state)
                st.session_state.results_analysis = analysis
                st.success("Results analysis complete!")
            else:
                st.warning("Please run simulation first")
    
    # Display analysis results
    if "data_quality_analysis" in st.session_state:
        st.markdown("### 📊 Data Quality Analysis")
        analysis = st.session_state.data_quality_analysis
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Quality Score", f"{analysis['quality_score']:.1%}")
        
        with col2:
            if analysis["issues"]:
                st.error("Issues Found:")
                for issue in analysis["issues"]:
                    st.write(f"• {issue}")
        
        if analysis["strengths"]:
            st.success("Strengths:")
            for strength in analysis["strengths"]:
                st.write(f"• {strength}")
        
        if analysis["recommendations"]:
            st.info("Recommendations:")
            for rec in analysis["recommendations"]:
                st.write(f"• {rec}")
    
    if "ai_recommendations" in st.session_state:
        st.markdown("### 🎯 AI Recommendations")
        recs = st.session_state.ai_recommendations
        
        st.markdown(f"**Workflow:** {recs['workflow_recommendation']}")
        st.markdown(f"**Distribution Method:** {recs['distribution_method']}")
        st.markdown(f"**Step Sizes:** {recs['step_sizes']}")
        
        st.markdown("**Reasoning:**")
        for reason in recs["reasoning"]:
            st.write(f"• {reason}")
    
    if "results_analysis" in st.session_state:
        st.markdown("### 📈 Results Analysis")
        analysis = st.session_state.results_analysis
        
        performance_colors = {
            "excellent": "green",
            "good": "blue", 
            "fair": "orange",
            "poor": "red"
        }
        
        st.markdown(f"**Performance Level:** :{performance_colors.get(analysis['performance_level'], 'gray')}[{analysis['performance_level'].title()}]")
        
        if analysis["key_insights"]:
            st.markdown("**Key Insights:**")
            for insight in analysis["key_insights"]:
                st.write(f"• {insight}")
        
        if analysis["optimization_opportunities"]:
            st.markdown("**Optimization Opportunities:**")
            for opp in analysis["optimization_opportunities"]:
                st.write(f"• {opp}")
        
        if analysis["recommendations"]:
            st.markdown("**Recommendations:**")
            for rec in analysis["recommendations"]:
                st.write(f"• {rec}")
    
    # Export AI analysis
    if st.button("📤 Export AI Analysis"):
        report = ai_agent.export_ai_analysis()
        st.download_button(
            label="📥 Download AI Analysis Report",
            data=report,
            file_name="ai_analysis_report.json",
            mime="application/json"
        ) 