package com.optimized.paiementmanagement.controller;

import com.optimized.paiementmanagement.dto.CompteBancaireRequestDTO;
import com.optimized.paiementmanagement.dto.CompteBancaireResponseDTO;
import com.optimized.paiementmanagement.service.CompteBancaireService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;

/**
 * Bank Account Controller - Optimized
 */
@RestController
@RequestMapping("/api/comptes")
@RequiredArgsConstructor
@Slf4j
@Tag(name = "Bank Accounts", description = "Bank account management APIs")
public class CompteBancaireController {
    
    private final CompteBancaireService compteBancaireService;
    
    @PostMapping
    @Operation(summary = "Create a new bank account")
    public ResponseEntity<CompteBancaireResponseDTO> createCompte(@Valid @RequestBody CompteBancaireRequestDTO requestDTO) {
        log.info("REST request to create bank account: {}", requestDTO.getNumeroCompte());
        CompteBancaireResponseDTO response = compteBancaireService.createCompte(requestDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    @GetMapping("/<built-in function id>")
    @Operation(summary = "Get bank account by ID")
    public ResponseEntity<CompteBancaireResponseDTO> getCompteById(@PathVariable Long id) {
        log.info("REST request to get bank account: {}", id);
        CompteBancaireResponseDTO response = compteBancaireService.getCompteById(id);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/numero/{numeroCompte}")
    @Operation(summary = "Get bank account by account number")
    public ResponseEntity<CompteBancaireResponseDTO> getCompteByNumero(@PathVariable String numeroCompte) {
        log.info("REST request to get bank account by number: {}", numeroCompte);
        CompteBancaireResponseDTO response = compteBancaireService.getCompteByNumero(numeroCompte);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping
    @Operation(summary = "Get all bank accounts")
    public ResponseEntity<List<CompteBancaireResponseDTO>> getAllComptes() {
        log.info("REST request to get all bank accounts");
        List<CompteBancaireResponseDTO> responses = compteBancaireService.getAllComptes();
        return ResponseEntity.ok(responses);
    }
    
    @PatchMapping("/<built-in function id>/solde")
    @Operation(summary = "Update account balance")
    public ResponseEntity<CompteBancaireResponseDTO> updateSolde(
            @PathVariable Long id,
            @RequestParam BigDecimal solde) {
        log.info("REST request to update account {} balance", id);
        CompteBancaireResponseDTO response = compteBancaireService.updateSolde(id, solde);
        return ResponseEntity.ok(response);
    }
    
    @DeleteMapping("/<built-in function id>")
    @Operation(summary = "Delete bank account")
    public ResponseEntity<Void> deleteCompte(@PathVariable Long id) {
        log.info("REST request to delete bank account: {}", id);
        compteBancaireService.deleteCompte(id);
        return ResponseEntity.noContent().build();
    }
}
