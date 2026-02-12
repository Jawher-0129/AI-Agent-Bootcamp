package com.optimized.paiementmanagement.service;

import com.optimized.paiementmanagement.dto.PaiementRequestDTO;
import com.optimized.paiementmanagement.dto.PaiementResponseDTO;
import com.optimized.paiementmanagement.model.Paiement;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Payment Service Interface - Promotes Dependency Inversion Principle
 */
public interface PaiementService {
    
    PaiementResponseDTO createPaiement(PaiementRequestDTO requestDTO);
    
    PaiementResponseDTO getPaiementById(Long id);
    
    List<PaiementResponseDTO> getAllPaiements();
    
    List<PaiementResponseDTO> getPaiementsByReservationId(Long reservationId);
    
    List<PaiementResponseDTO> getPaiementsByDateRange(LocalDateTime startDate, LocalDateTime endDate);
    
    PaiementResponseDTO updatePaiementStatus(Long id, Paiement.PaiementStatus status);
    
    void deletePaiement(Long id);
}
