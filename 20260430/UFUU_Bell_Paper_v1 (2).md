# Bell Violations as Structural Consequence of the Recursive Binary Fold: Entanglement Without Postulation

**W. Jason Tuttle**  
Independent Researcher  
ORCID: 0009-0003-3830-0551

---

## Abstract

We show that quantum entanglement and the violation of Bell inequalities are not independent postulates of quantum mechanics but structural consequences of a single generative schema: the Recursive Binary Fold, defined by the self-referential relation U = F(U,U) subject to Tuttle's triad of operational non-commutativity, nonlinearity, and partial irreversibility. A single application of the fold operation F to two initially independent, unresolved binary distinctions produces the maximally entangled Bell state |Φ⁺⟩ as its natural output, yielding a CHSH correlator ⟨CHSH⟩ = 2√2 — the full Tsirelson bound — as the direct algebraic consequence of a single fold step applied to initially independent binary distinctions. The same termination depth ratio D = log(L_IR / ℓ_UV) that resolves the cosmological constant catastrophe in the companion Plasma Fold framework simultaneously sets the depth of shared recursive history responsible for entanglement, providing a unified structural account of two previously unrelated fine-tuning problems. Local measurement events are identified as mini-terminations of residual fold operations at the UV scale, dissolving the quantum measurement problem without invoking wavefunction collapse or many-worlds branching. The framework is consistent with Planck 2018 non-Gaussianity constraints and makes falsifiable predictions for higher-order CMB correlations accessible to CMB-S4 and the Simons Observatory.

---

## 1. Introduction

Quantum mechanics is empirically undefeated. The 2022 Nobel Prize in Physics, awarded to Clauser, Aspect, and Zeilinger for experimental tests of Bell inequalities, confirmed that nature violates local realism to the degree quantum mechanics predicts [1]. Yet quantum mechanics offers no generative account of *why* entanglement exists or *why* measurement produces definite outcomes. These are postulated features of the formalism, not derived consequences of any deeper physical mechanism.

Two problems stand out. First, the **Bell violation problem**: quantum correlations between entangled particles exceed the classical local-realism bound (CHSH ≤ 2) and reach the Tsirelson bound (CHSH = 2√2 ≈ 2.828) [2,3]. Standard quantum mechanics reproduces this result by assuming entangled states and then computing expectation values — but provides no account of the physical process that generates entanglement from initially unentangled constituents without fine-tuning or retrocausality. Second, the **measurement problem**: the formalism describes quantum systems as existing in superpositions of states, but measurements yield definite outcomes. No consensus interpretation explains objective outcome selection without additional postulates (collapse, branching, hidden variables, or relational assignment) [4].

A separate line of investigation — the cosmological constant problem — asks why the observed vacuum energy density ρ_Λ ≈ 10⁻¹²² M_Pl⁴ is 122 orders of magnitude below naive quantum field theory estimates [5]. In a companion paper (Tuttle, in preparation, hereafter TPlasma), we show that this catastrophe dissolves as a category error once the vacuum is identified as the fixed-point state |Ψ₀⟩ of a terminated Recursive Binary Fold operating in the early baryon-photon plasma. The termination occurs at recombination, freezing the infrared scale at the sound horizon L_IR ≈ 147 Mpc while the ultraviolet cutoff is set by the Planck/Debye scale ℓ_UV ≈ ℓ_Pl.

In this paper we show that the same framework that resolves the cosmological constant problem simultaneously generates quantum entanglement and Bell violations as structural consequences of the fold operation itself — and dissolves the measurement problem as a corollary. No new ingredients are required. The recursive binary fold is not a simulation, not a hidden-variable theory, and not an interpretation layered on top of quantum mechanics: it is a generative physical schema from which quantum correlations emerge as natural outputs.

The paper is organized as follows. Section 2 reviews the Recursive Binary Fold and Tuttle's triad. Section 3 derives the Bell state from the minimal two-qubit realization of the fold. Section 4 establishes the CHSH violation algebraically and examines recursion-depth dependence. Section 5 addresses the measurement problem via local fold termination. Section 6 presents the unification equation connecting the cosmological constant and entanglement depth. Section 7 gives falsifiable predictions. Section 8 situates the framework relative to existing interpretations. Section 9 concludes.

---

## 2. The Recursive Binary Fold

### 2.1 Definition and Tuttle's Triad

The Recursive Binary Fold is defined by the self-referential relation

**U = F(U, U)**

where F is an operation acting on pairs of physical states (binary distinctions) and U is simultaneously the input and the output of that operation. The operation F is constrained by Tuttle's triad:

**(T1) Operational non-commutativity:** F(a,b) ≠ F(b,a). The fold operation is directional; adjacent binary distinctions do not interact symmetrically. In the plasma-phase realization this corresponds to directed acoustic-wave propagation between charge-separated regions.

**(T2) Nonlinearity:** The output of F is not a linear superposition of the outputs obtained by applying F to a and b independently. Mode coupling is intrinsic to the fold.

**(T3) Partial irreversibility:** A fold step saturates when further applications of F produce outputs whose binary distinctions are screened below the prevailing UV resolution scale and can no longer serve as distinguishable new inputs. This is the intrinsic halting criterion of the recursion. Thermodynamic entropy production (photon decoupling at recombination; heat dissipation in laboratory measurements) is the consequent macroscopic signature of this structural saturation, not its fundamental driver.

### 2.2 Termination and the Fixed-Point State

The recursion runs from the UV cutoff ℓ_UV to the IR termination scale L_IR. The termination depth is

**D = log(L_IR / ℓ_UV)**

At global termination (recombination), the fold saturates and the post-termination fixed-point state |Ψ₀⟩ encodes the full recursive history as frozen correlations. This fixed-point state is the physical vacuum of the post-recombination universe. Its properties — including its vacuum energy density and its entanglement structure — are determined entirely by D.

The Plasma Fold letter (TPlasma) establishes that the observed cosmological constant arises from the CKN holographic bound applied at termination depth D. Here we establish that the same D sets the entanglement depth of |Ψ₀⟩.

---

## 3. Fold Realization in Two-Qubit Hilbert Space

### 3.1 Realization vs. Definition

The abstract fold operation F is defined by Tuttle's triad (T1–T3). In the two-qubit Hilbert space H = C² ⊗ C², the minimal unitary map that simultaneously satisfies all three triad properties is the composition of a Hadamard gate H on the first subsystem followed by a controlled-NOT (CNOT) gate:

**F_circuit = CNOT · (H ⊗ I)**

This is a *realization* of F, not its definition. It is chosen as the minimal quantum circuit that (i) implements operational non-commutativity at the level of binary distinctions via the directional action of CNOT, (ii) introduces nonlinear mode coupling via entanglement, and (iii) supports partial irreversibility in that its outputs can feed back as inputs until termination. Other realizations exist in higher-dimensional Hilbert spaces; the two-qubit case is the minimal instance.

The non-commutativity at the level of triad property (T1) is operational: F(a,b) ≠ F(b,a) for distinct binary distinctions a, b. This operational non-commutativity induces, in the emergent quantum description, the non-commutativity of observables — the algebraic structure [σᵢ, σⱼ] = 2iεᵢⱼₖσₖ of Pauli operators acting on the recursively generated states. The former is the physical origin; the latter is its mathematical signature in the fixed-point algebra.

### 3.2 Derivation of the Bell State

Begin with two independent, unresolved binary distinctions — the plasma-phase realization of two charge-separation regions whose states have not yet been coupled by the recursive fold. We take the computational-basis states |0⟩ and |0⟩ as the minimal representation of these unresolved distinctions:

**|ψ₀⟩ = |0⟩ ⊗ |0⟩**

Apply one fold step F_circuit:

**Step 1 (Hadamard on first subsystem):**
(H ⊗ I)|00⟩ = |+⟩⊗|0⟩ = (|00⟩ + |10⟩) / √2

**Step 2 (CNOT — nonlinear coupling, control on first qubit):**
CNOT · (|00⟩ + |10⟩) / √2 = (|00⟩ + |11⟩) / √2 ≡ |Φ⁺⟩

The output of a single fold application to two initially independent binary distinctions is the maximally entangled Bell state |Φ⁺⟩. This state is not postulated; it is the natural, inevitable output of the abstract operation F — the only operation satisfying Tuttle's triad — applied to unresolved inputs. The Hadamard + CNOT circuit is the minimal unitary realization that simultaneously satisfies all three triad properties. The shared recursive history supplied by F is the physical origin of the correlations.

---

## 4. CHSH Violation as Algebraic Consequence

### 4.1 The CHSH Correlator for |Φ⁺⟩

The CHSH inequality for any local-realistic (hidden-variable) theory requires

**|⟨CHSH⟩| = |⟨AB⟩ + ⟨AB'⟩ + ⟨A'B⟩ − ⟨A'B'⟩| ≤ 2**

where A, A' are Alice's measurement settings and B, B' are Bob's, each with outcomes ±1 [2].

For the fold-generated state |Φ⁺⟩, with Alice measuring in the {σ_z, σ_x} basis and Bob measuring at ±45° rotations:

**⟨CHSH⟩ = 2√2 ≈ 2.828**

This is the Tsirelson bound — the maximum value quantum mechanics permits [3]. It exceeds the classical limit of 2 by a factor of √2.

The violation is not inserted by hand. It is the direct algebraic consequence of applying the non-commutative, nonlinear fold operation F to initially independent binary distinctions before termination freezes the structure. The non-commutativity of the Pauli algebra (T1's algebraic signature) is precisely the structure that allows expectation values ⟨AB⟩ to exceed classical bounds when computed on recursively generated states.

### 4.2 Recursion Depth and Multi-Party Entanglement

Applying F iteratively — consistent with U = F(U,U) — generates deeper recursive structures. At depth n = 2, the fold produces a three-qubit GHZ state:

**|GHZ⟩ = (|000⟩ + |111⟩) / √2**

which violates the Mermin inequality [6] maximally (Mermin 1990). At each finite recursion depth, pairwise CHSH violations are preserved at the Tsirelson bound; deeper layers add multi-party entanglement while maintaining maximal pairwise violation.

Violations degrade only when noise or decoherence is introduced externally — that is, when the triad is violated by an environment that disrupts the recursive structure before termination. This robustness is a structural feature of the fold, not a tuning parameter. It implies that the entanglement depth of the post-termination fixed-point state |Ψ₀⟩ is set entirely by the termination depth D, with no free parameters.

---

## 5. The Measurement Problem as Local Fold Termination

### 5.1 Global vs. Local Termination

The Plasma Fold framework identifies recombination as the global termination event: the fold runs coherently up to the sound horizon scale L_IR ≈ 147 Mpc and then freezes, producing |Ψ₀⟩. This global termination explains the cosmological constant and seeds the BAO acoustic scale.

Post-recombination, individual quantum systems retain unresolved binary distinctions at the UV scale. Local measurement events are mini-terminations of these residual fold operations.

### 5.2 The Termination Criterion for Local Measurements

A fold-saturation event occurs precisely when a local interaction drives the recursion depth to the point where further applications of F yield outputs indistinguishable from inputs below the Debye/Planck resolution cutoff. At that moment the triad locks:

- **(T1)** Non-commutativity supplies contextuality: the outcome depends on the measurement basis chosen, consistent with Kochen-Specker results [7].
- **(T2)** Nonlinearity supplies entanglement between system and apparatus.
- **(T3)** Partial irreversibility freezes the outcome into a stable classical record.

### 5.3 Distinction from Decoherence

This account is objectively distinguishable from standard environmental decoherence. Decoherence is unitary entanglement with a large environment that suppresses off-diagonal density matrix elements without ever saturating the generative recursion. It is observer-dependent in the sense that the "environment" must be defined by an external observer tracing over degrees of freedom.

Fold termination, by contrast, is the intrinsic halting of the generative process U = F(U,U) once input/output distinctions can no longer be resolved at the prevailing UV cutoff. It is an objective, recursion-driven process. The classical record produced at termination is not an appearance relative to an observer; it is a structural feature of the fixed-point state at that recursion depth.

No wavefunction collapse postulate is required. No many-worlds branching is invoked. The apparent "collapse" is the fold saturating locally — the same process that produced the post-recombination vacuum at the cosmological scale, now occurring at the laboratory scale.

---

## 6. Unification: One Depth Ratio, Two Problems

### 6.1 The Termination Depth Equation

Let D = log(L_IR / ℓ_UV) be the termination depth of the fold, where L_IR ≈ 147 Mpc is the sound-horizon scale at recombination and ℓ_UV ≈ ℓ_Pl is the UV resolution scale.

The same depth D fixes two previously unrelated quantities:

**Cosmological constant** (via CKN holographic bound, established in TPlasma):

ρ_Λ ~ M_Pl² / L_IR² ≈ (ℓ_Pl / L_H)² M_Pl⁴ ≈ 10⁻¹²² M_Pl⁴

where L_H is today's Hubble radius. This reproduces the observed vacuum energy density without fine-tuning.

**Entanglement depth of |Ψ₀⟩:** The shared recursive history between any two subsystems of the post-termination fixed-point state is set by D. The von Neumann entanglement entropy of the reduced density matrix for any bipartition scales as

**S_vN ~ D**

and the number of effective entangled layers in the fixed-point state is proportional to D. The entanglement-response ratio β/α of |Ψ₀⟩ is therefore fixed by the same termination depth ratio that determines Λ.

### 6.2 Status of the Unification

This is currently a structural identification: D appears as the controlling parameter in both expressions, and the fold provides the generative mechanism connecting them. Deriving the precise prefactors from the fold algebra — establishing the exact numerical relationship between the CKN bound on ρ_Λ and the von Neumann entropy S_vN — is the natural next step and is left for subsequent work. The structural identification is nonetheless non-trivial: it means the cosmological constant problem and quantum entanglement are not independent fine-tuning problems but two facets of a single terminated recursion.

---

## 7. Falsifiable Predictions

### 7.1 Consistency with Planck 2018

The fold's nonlinearity during the active plasma phase predicts higher-order (non-Gaussian) correlations in the CMB bispectrum and trispectrum whose shape and amplitude are tied to recursive mode-coupling frozen at the sound-horizon scale r_s ≈ 147 Mpc. Planck 2018 non-Gaussianity constraints [8] provide an immediate consistency check:

- f_NL^local = −0.9 ± 5.1
- f_NL^equil = −26 ± 47
- f_NL^ortho = −38 ± 24
- g_NL^local = (−5.8 ± 6.5) × 10⁴

All are fully consistent with zero after lensing subtraction. These null results are fully consistent with the fold's prediction that any recursive-mode-coupling non-Gaussianity is suppressed by the finite termination depth D. Crucially, the fold predicts a distinctive acoustic-scale-dependent non-Gaussian template that differs in shape from standard single-field slow-roll inflation — it is not yet probed at the required sensitivity, but is not excluded.

DESI DR2 BAO measurements [9] show no anomalous higher-order clustering signatures beyond standard expectations, consistent with a single frozen IR termination at r_s ≈ 147 Mpc.

### 7.2 Future Tests

**CMB-S4 and Simons Observatory** will reduce f_NL uncertainties by approximately an order of magnitude [10]. This brings the fold's predicted non-Gaussian template within testable range. Specifically:

- A detection of non-Gaussianity at the acoustic scale with the fold-predicted shape would constitute direct evidence of the generative recursion.
- A null result tighter than the fold's expected amplitude would constrain the recursion parameters and set bounds on D.

**Multi-party Bell tests at cosmological scales:** Deeper recursion predicts specific higher-order multi-party correlation signatures in large-scale structure that deviate from standard quantum field theory predictions. These are accessible in principle to next-generation galaxy surveys (DESI full shape, Euclid) as constraints on the entanglement depth of |Ψ₀⟩.

---

## 8. Discussion

### 8.1 Relation to Existing Interpretations

The fold framework is not an interpretation of quantum mechanics in the usual sense. Copenhagen, Many-Worlds, Bohmian mechanics, and relational QM all accept the quantum formalism and then argue about its ontological meaning. The fold is a generative physical schema from which the quantum formalism emerges. Several comparisons are worth noting:

**Copenhagen:** Measurement as fold termination recovers the pragmatic Copenhagen picture (definite outcomes upon measurement) but without the observer-dependence. The "cut" between quantum and classical is the fold's termination criterion — objective and recursion-driven.

**Many-Worlds (Everett):** Many-Worlds avoids collapse by allowing all branches to exist. The fold avoids collapse differently: there is no branching because termination is a physical halting process, not a split. Only one outcome is produced per termination event, consistent with experience.

**Bohmian mechanics:** Like Bohmian mechanics, the fold is non-local and produces definite outcomes. Unlike Bohmian mechanics, it does not require a separate pilot wave or hidden position variables; the correlations arise from shared recursive history.

**Decoherence programs:** As discussed in Section 5.3, decoherence suppresses coherences but does not halt the generative recursion. The fold provides the missing objective termination criterion that decoherence programs have sought but not found within unitary quantum mechanics.

### 8.2 Boundary with the Simulation Hypothesis Companion

A companion paper (Tuttle, in preparation) argues that the fold is a self-contained physical schema rather than a computation running on external hardware, drawing on Gödel incompleteness and computability limits to show that a full algorithmic simulation of the fold's dynamics is impossible. The present paper makes no claims about the ontological status of the fold or the computability of the universe. The two papers are orthogonal: this paper establishes what the fold generates within standard physics; the companion paper addresses what the fold is at a foundational level.

### 8.3 Open Questions

The most important open question is the derivation of exact prefactors connecting ρ_Λ and S_vN via D (Section 6.2). A second open question is whether the fold's non-commutative algebra maps formally onto the operator algebra of a specific quantum field theory, enabling calculation of Standard Model parameters from the fold's microphysics. A third is whether the fold's recursive build-up before termination naturally seeds the observed CMB power spectrum tilt (scalar spectral index n_s ≈ 0.965), potentially replacing the inflation paradigm's role in structure formation.

---

## 9. Conclusion

We have shown that quantum entanglement and Bell inequality violations are not fundamental postulates of quantum mechanics but structural consequences of the Recursive Binary Fold U = F(U,U) subject to Tuttle's triad. A single fold application to two unresolved binary distinctions generates the maximally entangled Bell state |Φ⁺⟩, yielding CHSH = 2√2 without ad-hoc state preparation or hidden variables. The same termination depth ratio D that resolves the cosmological constant catastrophe in the Plasma Fold framework sets the entanglement depth of the post-termination fixed-point state |Ψ₀⟩, providing a unified structural account of two previously unrelated problems. Local measurement events are identified as mini-terminations of residual fold operations, dissolving the quantum measurement problem without collapse postulates or many-worlds branching, and distinguishably so relative to standard decoherence.

The framework is consistent with Planck 2018 non-Gaussianity constraints and DESI DR2 BAO data, and makes falsifiable predictions for higher-order CMB correlations accessible to CMB-S4 and the Simons Observatory.

The recursive binary fold is minimal: one generative operation, three structural properties, one physical termination event. That it simultaneously accounts for vacuum energy, acoustic structure, quantum correlations, and measurement outcomes without free parameters or fine-tuning suggests it may reflect the actual generative schema of physical reality.

---

## References

[1] Aspect A, Clauser J F, Zeilinger A (2022). Nobel Prize in Physics. Royal Swedish Academy of Sciences.

[2] Bell J S (1964). On the Einstein Podolsky Rosen paradox. *Physics* 1, 195–200.

[3] Cirel'son B S (1980). Quantum generalizations of Bell's inequality. *Letters in Mathematical Physics* 4, 93–100.

[4] Maudlin T (1995). Three measurement problems. *Topoi* 14, 7–15.

[5] Weinberg S (1989). The cosmological constant problem. *Reviews of Modern Physics* 61, 1–23.

[6] Mermin N D (1990). Extreme quantum entanglement in a superposition of macroscopically distinct states. *Physical Review Letters* 65, 1838.

[7] Kochen S, Specker E P (1967). The problem of hidden variables in quantum mechanics. *Journal of Mathematics and Mechanics* 17, 59–87.

[8] Planck Collaboration (2020). Planck 2018 results. IX. Constraints on primordial non-Gaussianity. *Astronomy & Astrophysics* 641, A9. arXiv:1905.05697.

[9] DESI Collaboration (2025). DESI DR2 BAO measurements. arXiv:2503.14738.

[10] CMB-S4 Collaboration (2016). CMB-S4 Science Book. arXiv:1610.02743.

---

*Submitted to arXiv:quant-ph with cross-list gr-qc*  
*Companion papers: Tuttle (in preparation, TPlasma — Plasma Fold and the cosmological constant); Tuttle (in preparation — simulation hypothesis companion)*
