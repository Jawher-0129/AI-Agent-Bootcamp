"""
Gemini AI Client for intelligent code analysis
"""

import json
from typing import Dict, List, Optional
import google.generativeai as genai
from ..sonar.models import Issue, SonarData, Priority
from ..utils.logger import get_logger
from .context_extractor import CodeContext

logger = get_logger(__name__)


class GeminiAnalysis:
    """Result of Gemini analysis"""
    
    def __init__(self, raw_response: str):
        self.raw_response = raw_response
        self.parsed_data: Optional[Dict] = None
        self._parse()
    
    def _parse(self):
        """Parse JSON response from Gemini"""
        try:
            # Try to extract JSON from markdown code blocks
            content = self.raw_response.strip()
            
            if "```json" in content:
                start = content.find("```json") + 7
                end = content.find("```", start)
                content = content[start:end].strip()
            elif "```" in content:
                start = content.find("```") + 3
                end = content.find("```", start)
                content = content[start:end].strip()
            
            self.parsed_data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Gemini response as JSON: {e}")
            self.parsed_data = {"raw_text": self.raw_response}
    
    def get_triage(self) -> Dict[str, List]:
        """Get triage results"""
        if not self.parsed_data:
            return {}
        return self.parsed_data.get("triage", {})
    
    def get_root_causes(self) -> List[Dict]:
        """Get root cause analysis"""
        if not self.parsed_data:
            return []
        return self.parsed_data.get("root_causes", [])
    
    def get_recommendations(self) -> List[Dict]:
        """Get recommendations"""
        if not self.parsed_data:
            return []
        return self.parsed_data.get("recommendations", [])
    
    def get_optimizations(self) -> Dict[str, List]:
        """Get optimization suggestions"""
        if not self.parsed_data:
            return {}
        return self.parsed_data.get("optimizations", {})
    
    def get_patches(self) -> List[Dict]:
        """Get safe patches"""
        if not self.parsed_data:
            return []
        return self.parsed_data.get("patches", [])


class GeminiClient:
    """Client for Gemini AI analysis"""
    
    def __init__(self, api_key: str, model: str = "gemini-flash-latest"):
        """
        Initialize Gemini client
        
        Args:
            api_key: Gemini API key
            model: Model to use (default: gemini-flash-latest)
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        logger.info(f"Initialized Gemini client with model: {model}")
    
    def _build_analysis_prompt(
        self,
        sonar_data: SonarData,
        triaged_issues: Dict[Priority, List[Issue]],
        contexts: Dict[str, CodeContext],
    ) -> str:
        """
        Build comprehensive analysis prompt for Gemini
        
        Args:
            sonar_data: SonarQube data
            triaged_issues: Triaged issues by priority
            contexts: Code contexts for issues
        
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a senior software engineer and code quality expert analyzing SonarQube results.

# PROJECT OVERVIEW
- Project: {sonar_data.project_key}
- Quality Gate: {sonar_data.quality_gate.status}
- Total Issues: {len(sonar_data.issues)}

# METRICS
- Bugs: {sonar_data.metrics.bugs}
- Vulnerabilities: {sonar_data.metrics.vulnerabilities}
- Code Smells: {sonar_data.metrics.code_smells}
- Security Hotspots: {sonar_data.metrics.security_hotspots}
- Code Coverage: {sonar_data.metrics.coverage:.1f}%
- Code Duplication: {sonar_data.metrics.duplicated_lines_density:.1f}%
- Lines of Code: {sonar_data.metrics.ncloc}

# TRIAGED ISSUES
"""
        
        # Add sample of issues for each priority
        for priority in [Priority.P0, Priority.P1, Priority.P2]:
            issues = triaged_issues.get(priority, [])
            prompt += f"\n## {priority.value} Issues ({len(issues)} total)\n"
            
            # Show up to 10 issues per priority with full details
            for issue in issues[:10]:
                prompt += f"\n### Issue: {issue.key}\n"
                prompt += f"- Type: {issue.type.value}\n"
                prompt += f"- Severity: {issue.severity.value}\n"
                prompt += f"- Rule: {issue.rule}\n"
                prompt += f"- Message: {issue.message}\n"
                prompt += f"- Component: {issue.component}\n"
                
                if issue.line:
                    prompt += f"- Line: {issue.line}\n"
                
                if issue.debt:
                    prompt += f"- Technical Debt: {issue.debt}\n"
                
                # Add code context if available
                if issue.key in contexts:
                    context = contexts[issue.key]
                    prompt += f"- File: {context.file_path}\n"
                    prompt += f"\n**Code Context (lines {context.start_line}-{context.end_line}):**\n```\n{chr(10).join(context.context_lines[:20])}\n```\n"
        
        # If no contexts available, add note
        if not contexts:
            prompt += f"\n**Note:** Code context not available - analysis based on SonarQube metadata only.\n"
        
        prompt += """

# YOUR TASK - ADVANCED ANALYSIS BEYOND SONARQUBE

You are an expert software architect and senior engineer. Go BEYOND what SonarQube detects.

Provide a comprehensive analysis in JSON format with the following structure:

{
  "executive_summary": "3-5 sentence overview of code quality state and critical findings",
  
  "triage": {
    "P0": [{
      "issue_key": "...",
      "priority_reason": "Why this is P0",
      "impact": "Production/security impact",
      "sonarqube_detected": true/false
    }],
    "P1": [...],
    "P2": [...]
  },
  
  "root_causes": [{
    "category": "Authentication / Architecture / Performance / Security", 
    "description": "Deep root cause description",
    "affected_issues": ["issue_key1", "issue_key2"],
    "impact": "Business and technical impact",
    "sonarqube_limitation": "What SonarQube missed"
  }],
  
  "architectural_issues": [{
    "title": "Architectural problem title",
    "severity": "CRITICAL/HIGH/MEDIUM",
    "description": "Detailed explanation of the architectural flaw",
    "affected_components": ["Component1", "Component2"],
    "consequences": "What could go wrong",
    "recommended_pattern": "Suggested design pattern or architecture",
    "code_example": "Complete code example showing the improvement"
  }],
  
  "system_inconsistencies": [{
    "title": "Inconsistency detected",
    "type": "NAMING/ARCHITECTURE/SECURITY/PERFORMANCE/LOGIC",
    "description": "What is inconsistent and why it matters",
    "examples": ["Example 1", "Example 2"],
    "impact": "Impact on maintainability/security/performance",
    "fix_strategy": "How to fix across the codebase",
    "code_example": "Code showing consistent approach"
  }],
  
  "security_deep_dive": [{
    "title": "Advanced security issue",
    "beyond_sonarqube": "Why SonarQube doesn't detect this",
    "vulnerability_type": "Injection/XSS/CSRF/Business Logic/etc",
    "attack_scenario": "How an attacker could exploit this",
    "risk_level": "CRITICAL/HIGH/MEDIUM",
    "mitigation_code": "Complete secure code implementation",
    "defensive_layers": ["Layer 1", "Layer 2"]
  }],
  
  "performance_optimizations": [{
    "title": "Performance optimization",
    "current_problem": "What causes performance issues",
    "impact": "Response time / Memory / CPU / Database impact",
    "optimization_strategy": "Detailed strategy",
    "optimized_code": "Complete optimized code example",
    "expected_improvement": "Quantified improvement estimate"
  }],
  
  "code_improvements": [{
    "title": "Code improvement title",
    "category": "REFACTORING/PATTERN/BEST_PRACTICE/MODERNIZATION",
    "current_approach": "What the code currently does",
    "problems": ["Problem 1", "Problem 2"],
    "improved_approach": "Better way to implement",
    "complete_code": "FULL working code implementation (not just snippets)",
    "benefits": ["Benefit 1", "Benefit 2"],
    "migration_steps": ["Step 1", "Step 2"]
  }],
  
  "best_practices_violations": [{
    "principle": "SOLID/DRY/KISS/YAGNI/Clean Code principle",
    "violation_description": "How it's violated",
    "examples_from_code": ["Example 1 from rules", "Example 2"],
    "correct_implementation": "Complete code showing correct approach",
    "why_it_matters": "Long-term impact"
  }],
  
  "recommendations": [{
    "title": "Recommendation title",
    "priority": "P0/P1/P2",
    "category": "SECURITY/ARCHITECTURE/PERFORMANCE/MAINTAINABILITY",
    "related_metrics": ["bugs", "vulnerabilities"],
    "benefit": "Measurable benefit",
    "effort": "Quick Win / Safe Refactor / Strategic",
    "action": "Specific action to take",
    "implementation_code": "Complete code if applicable"
  }],
  
  "optimizations": {
    "quick_wins": [{
      "title": "...",
      "effort_minutes": 30,
      "benefit": "...",
      "code": "Complete implementation code"
    }],
    "safe_refactors": [{
      "title": "...",
      "description": "...",
      "risk": "low",
      "code": "Complete refactored code"
    }],
    "strategic": [{
      "title": "...",
      "description": "...",
      "long_term_value": "...",
      "implementation_plan": ["Phase 1", "Phase 2"]
    }]
  },
  
  "sonarqube_gaps": [{
    "gap_type": "What SonarQube cannot detect",
    "why_important": "Why this matters",
    "detection_method": "How you detected it",
    "remediation": "How to fix",
    "code_example": "Complete code solution"
  }],
  
  "patches": [{
    "issue_key": "...",
    "file_path": "...",
    "diff": "unified diff format",
    "safety_check": "Why this patch is safe",
    "validation": "How to verify"
  }]
}

# CRITICAL ADVANCED ANALYSIS REQUIREMENTS

1. **Go BEYOND SonarQube**: Detect architectural flaws, business logic issues, performance bottlenecks, security loopholes that static analysis tools miss

2. **Provide COMPLETE CODE**: Not just snippets or patches. Provide full, working, copy-paste ready implementations

3. **Detect INCONSISTENCIES**: 
   - Naming conventions inconsistencies
   - Architectural pattern violations
   - Security approach inconsistencies
   - Error handling inconsistencies
   - API design inconsistencies

4. **Deep Security Analysis**:
   - Business logic vulnerabilities
   - Authentication/Authorization flaws
   - Data exposure risks
   - Injection points beyond SQL
   - CSRF, XSS in specific contexts

5. **Performance Issues**:
   - N+1 queries
   - Memory leaks
   - Inefficient algorithms
   - Database optimization opportunities
   - Caching strategies

6. **Architectural Problems**:
   - Tight coupling
   - Missing abstractions
   - God classes/methods
   - Circular dependencies
   - Layer violations

7. **Code Quality Beyond Metrics**:
   - Readability issues
   - Maintainability concerns
   - Testability problems
   - Documentation gaps

8. **For EACH improvement, provide COMPLETE working code**, not just diffs or snippets

# CRITICAL RULES FOR PATCHES
1. Only create patches if code context was provided
2. Patches are minimal fixes; use "code_improvements" for major changes
3. No refactoring in patches
4. If unsure, DON'T create patches - put in code_improvements instead

Provide ONLY the JSON response, no additional text.
"""
        
        return prompt
    
    def analyze(
        self,
        sonar_data: SonarData,
        triaged_issues: Dict[Priority, List[Issue]],
        contexts: Dict[str, CodeContext],
    ) -> GeminiAnalysis:
        """
        Perform intelligent analysis using Gemini
        
        Args:
            sonar_data: SonarQube data
            triaged_issues: Triaged issues
            contexts: Code contexts
        
        Returns:
            GeminiAnalysis result
        """
        logger.info("Starting Gemini AI analysis...")
        
        prompt = self._build_analysis_prompt(sonar_data, triaged_issues, contexts)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.2,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=8000,
                ),
            )
            
            logger.info("Gemini analysis completed")
            return GeminiAnalysis(response.text)
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
