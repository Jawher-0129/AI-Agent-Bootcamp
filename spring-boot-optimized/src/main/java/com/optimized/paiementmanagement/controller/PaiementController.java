package com.optimized.paiementmanagement.controller;

import com.optimized.paiementmanagement.dto.PaiementRequestDTO;
import com.optimized.paiementmanagement.dto.PaiementResponseDTO;
import com.optimized.paiementmanagement.model.Paiement;
import com.optimized.paiementmanagement.service.PaiementService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Payment Controller - Optimized with:
 * - Constructor injection (final fields)
 * - Proper HTTP status codes
 * - OpenAPI documentation
 * - Request validation
 */
@RestController
@RequestMapping("/api/paiements")
@RequiredArgsConstructor
@Slf4j
@Tag(name = "Payments", description = "Payment management APIs")
public class PaiementController {
    
    private final PaiementService paiementService;
    
    @PostMapping
    @Operation(summary = "Create a new payment")
    public ResponseEntity<PaiementResponseDTO> createPaiement(@Valid @RequestBody PaiementRequestDTO requestDTO) {
        log.info("REST request to create payment for reservation: {}", requestDTO.getReservationId());
        PaiementResponseDTO response = paiementService.createPaiement(requestDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    @GetMapping("/<built-in function id>")
    @Operation(summary = "Get payment by ID")
    public ResponseEntity<PaiementResponseDTO> getPaiementById(@PathVariable Long id) {
        log.info("REST request to get payment: {}", id);
        PaiementResponseDTO response = paiementService.getPaiementById(id);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping
    @Operation(summary = "Get all payments")
    public ResponseEntity<List<PaiementResponseDTO>> getAllPaiements() {
        log.info("REST request to get all payments");
        List<PaiementResponseDTO> responses = paiementService.getAllPaiements();
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/reservation/{reservationId}")
    @Operation(summary = "Get payments by reservation ID")
    public ResponseEntity<List<PaiementResponseDTO>> getPaiementsByReservation(@PathVariable Long reservationId) {
        log.info("REST request to get payments for reservation: {}", reservationId);
        List<PaiementResponseDTO> responses = paiementService.getPaiementsByReservationId(reservationId);
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/date-range")
    @Operation(summary = "Get payments by date range")
    public ResponseEntity<List<PaiementResponseDTO>> getPaiementsByDateRange(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endDate) {
        log.info("REST request to get payments between {} and {}", startDate, endDate);
        List<PaiementResponseDTO> responses = paiementService.getPaiementsByDateRange(startDate, endDate);
        return ResponseEntity.ok(responses);
    }
    
    @PatchMapping("/<built-in function id>/status")
    @Operation(summary = "Update payment status")
    public ResponseEntity<PaiementResponseDTO> updatePaiementStatus(
            @PathVariable Long id,
            @RequestParam Paiement.PaiementStatus status) {
        log.info("REST request to update payment {} status to {}", id, status);
        PaiementResponseDTO response = paiementService.updatePaiementStatus(id, status);
        return ResponseEntity.ok(response);
    }
    
    @DeleteMapping("/<built-in function id>")
    @Operation(summary = "Delete payment")
    public ResponseEntity<Void> deletePaiement(@PathVariable Long id) {
        log.info("REST request to delete payment: {}", id);
        paiementService.deletePaiement(id);
        return ResponseEntity.noContent().build();
    }
}
