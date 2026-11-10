"""Shared paper list for the deck and the report."""

LIT = [
("Evaluating the Robustness of Reinforcement Learning-based Adaptive Traffic Signal Control, "
 "arXiv:2603.15283, 2026",
 "Stress-tests trained RL signal controllers under demand surges, detector faults and "
 "distribution shift on standard benchmarks.",
 "Evaluation study only; no controller is proposed that retains performance once the demand "
 "distribution changes."),
("Human-Centric Traffic Signal Control for Equity, arXiv:2602.02959, 2026",
 "Adds fairness terms to the RL reward so that delay is distributed more evenly across "
 "approaches instead of minimising the network mean alone.",
 "Single-junction focus; fairness is not extended to corridor coordination or to priority "
 "vehicles."),
("Benchmarking Traffic Signal Control Robustness under Incidents, European Transport Research "
 "Review (Springer), 2026",
 "Benchmarks learned and rule-based controllers under lane blockages and incident-induced "
 "capacity loss.",
 "Homogeneous lane-based traffic assumed; results are not transferable to lane-less "
 "heterogeneous streams."),
("Intelligent Traffic Signal Control Based on Reinforcement Learning: A Survey, Artificial "
 "Intelligence Review (Springer), 2025",
 "Surveys state, action and reward formulations and multi-agent structures used in RL signal "
 "control.",
 "Reports that generalisation across time-of-day and demand regimes remains an open problem; "
 "offers no solution."),
("Traffic Signal Control via Reinforcement Learning: A Review on Applications and Innovations, "
 "Infrastructures (MDPI), 2025",
 "Reviews deployment-oriented RL signal control, including sensing requirements and "
 "safety considerations.",
 "Notes the absence of enforced safety constraints in most reported work; no implementation "
 "is provided."),
("Advances in Reinforcement Learning for Traffic Signal Control, Intelligent Transportation "
 "Infrastructure (Oxford), 2025",
 "Consolidates recent progress in value-based and policy-gradient controllers and their "
 "simulation environments.",
 "Comparisons use identical training and testing demand; robustness of the compared methods "
 "is not assessed."),
("Hierarchical Reinforcement Learning-based Traffic Signal Control, Scientific Reports, 2025",
 "Uses a high-level policy to select a phase strategy and a low-level policy to set duration, "
 "reducing the effective action space.",
 "Hierarchy is trained centrally; scaling to many junctions and emergency priority are "
 "not addressed."),
("Adaptive Traffic Signal Control Using Deep Reinforcement Learning: A Multi-Objective "
 "Approach, IATSS Research, 2025",
 "Optimises delay, queue length and emissions jointly through a weighted multi-objective "
 "reward.",
 "Objective weights are fixed by hand; no mechanism adapts them when the demand pattern "
 "changes."),
("Constrained Multi-Agent Reinforcement Learning for Autonomous Traffic Signal Control, "
 "arXiv:2503.23626, 2025",
 "Formulates signal control as a constrained MARL problem with explicit constraints on "
 "phase behaviour.",
 "Constraints are learned as soft penalties, so minimum-green and clearance intervals are "
 "not guaranteed at run time."),
("A Survey of Continual Reinforcement Learning, arXiv:2506.21872, 2025",
 "Reviews methods that allow an agent to keep learning under non-stationary conditions "
 "without catastrophic forgetting.",
 "General machine learning survey; contains no traffic-domain evaluation or deployment "
 "procedure."),
("Dynamic Traffic Signal Control for Heterogeneous Traffic Conditions Using Max Pressure and "
 "Reinforcement Learning, Expert Systems with Applications, 2024",
 "Combines max-pressure with RL for Indian lane-less traffic; demand represented in PCU.",
 "Junctions are controlled independently; no corridor coordination and no priority handling."),
("Emergency Vehicle Signal Preemption Considering Queue Spillbacks and Impacts on "
 "Non-priority Traffic, IET Intelligent Transport Systems, 2024",
 "Quantifies the delay imposed on cross traffic by conventional emergency pre-emption and "
 "proposes spillback-aware timing.",
 "Rule-based and single-corridor; not integrated with a learning controller or with routine "
 "coordination."),
("LibSignal: An Open Library for Traffic Signal Control, Machine Learning (Springer), 2023",
 "Provides a unified benchmark across SUMO and CityFlow for comparing RL and classical "
 "controllers.",
 "Benchmark scenarios are lane-based and Western; heterogeneous PCU traffic is not "
 "represented."),
("Representational Communication for Large-scale Traffic Signal Control, arXiv:2310.02435, 2023",
 "Learns compact messages exchanged between neighbouring agents to support scalable "
 "coordination.",
 "Message content is learned and opaque, making the resulting coordination difficult to "
 "verify or audit."),
("EMVLight: Multi-Agent Reinforcement Learning for Emergency Vehicle Routing and Traffic "
 "Signal Control, Transportation Research Part C, 2022",
 "Jointly learns emergency-vehicle routing and signal control to reduce response time.",
 "Requires control of vehicle routing; recovery of cross-street traffic after the emergency "
 "passes is not evaluated."),
("A Practical Guide to Multi-Objective Reinforcement Learning and Planning, JAAMAS, 2022",
 "Sets out formulations and solution methods for RL problems with conflicting objectives.",
 "Domain-independent; gives no guidance on balancing throughput against priority-vehicle "
 "delay in signal control."),
("Comparative Study of Algorithms for Optimized Traffic Signal Control in Bengaluru, "
 "arXiv:2109.00937, 2021",
 "Compares fixed-time, actuated and optimisation-based control on Bengaluru junction data.",
 "Limited to isolated junctions; no learning component and no coordination between signals."),
("Deep Reinforcement Learning for Fair Traffic Signal Control, IEEE ITSC, 2021",
 "Introduces fairness-aware rewards that bound the maximum waiting time on any approach.",
 "Evaluated on synthetic homogeneous demand; behaviour under Indian mixed traffic is "
 "not established."),
("Multi-Agent Deep Reinforcement Learning for Large-scale Traffic Signal Control (MA2C), "
 "IEEE Transactions on Intelligent Transportation Systems, 2020",
 "Decentralised advantage actor-critic with neighbour state sharing and spatial reward "
 "discounting.",
 "Stationary demand assumed; no safety enforcement layer and no emergency priority."),
("CoLight: Learning Network-level Cooperation for Traffic Signal Control, ACM CIKM, 2019",
 "Graph attention network lets each junction weight the influence of its neighbours "
 "during learning.",
 "Requires a jointly trained network-wide model; a single junction cannot be retrained "
 "or updated independently."),
]


REFS = [
"M. Aslani et al., “Evaluating the Robustness of Reinforcement Learning-based Adaptive Traffic Signal Control,” arXiv:2603.15283, 2026.",
"“Human-Centric Traffic Signal Control for Equity,” arXiv:2602.02959, 2026.",
"“Benchmarking Traffic Signal Control Robustness under Incidents,” European Transport Research Review, Springer, 2026.",
"“Intelligent Traffic Signal Control Based on Reinforcement Learning: A Survey,” Artificial Intelligence Review, Springer, 2025.",
"“Traffic Signal Control via Reinforcement Learning: A Review on Applications and Innovations,” Infrastructures, MDPI, vol. 10, 2025.",
"“Advances in Reinforcement Learning for Traffic Signal Control,” Intelligent Transportation Infrastructure, Oxford University Press, 2025.",
"“Hierarchical Reinforcement Learning-based Traffic Signal Control,” Scientific Reports, 2025.",
"“Adaptive Traffic Signal Control Using Deep Reinforcement Learning: A Multi-Objective Approach,” IATSS Research, 2025.",
"“Constrained Multi-Agent Reinforcement Learning for Autonomous Traffic Signal Control,” arXiv:2503.23626, 2025.",
"“A Survey of Continual Reinforcement Learning,” arXiv:2506.21872, 2025.",
"“Dynamic Traffic Signal Control for Heterogeneous Traffic Conditions Using Max Pressure and Reinforcement Learning,” Expert Systems with Applications, 2024.",
"J. Chen et al., “Emergency Vehicle Signal Preemption Considering Queue Spillbacks and Impacts on Non-priority Traffic,” IET Intelligent Transport Systems, 2024.",
"H. Mei et al., “LibSignal: An Open Library for Traffic Signal Control,” Machine Learning, Springer, 2023.",
"“Representational Communication for Large-scale Traffic Signal Control,” arXiv:2310.02435, 2023.",
"H. Su et al., “EMVLight: Multi-Agent Reinforcement Learning for Emergency Vehicle Routing and Traffic Signal Control,” Transportation Research Part C, 2022.",
"C. F. Hayes et al., “A Practical Guide to Multi-Objective Reinforcement Learning and Planning,” JAAMAS, vol. 36, 2022.",
"“Comparative Study of Algorithms for Optimized Traffic Signal Control in Bengaluru,” arXiv:2109.00937, 2021.",
"M. Raeis and A. Leon-Garcia, “Deep Reinforcement Learning for Fair Traffic Signal Control,” IEEE ITSC, 2021.",
"T. Chu et al., “Multi-Agent Deep Reinforcement Learning for Large-scale Traffic Signal Control,” IEEE Trans. Intelligent Transportation Systems, vol. 21, 2020.",
"H. Wei et al., “CoLight: Learning Network-level Cooperation for Traffic Signal Control,” ACM CIKM, 2019.",
"Indian Roads Congress, IRC 106-1990: Guidelines for Capacity of Urban Roads in Plain Areas.",
]
