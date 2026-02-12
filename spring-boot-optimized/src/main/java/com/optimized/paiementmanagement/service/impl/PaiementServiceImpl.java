package com.optimized.paiementmanagement.service.impl;

import com.optimized.paiementmanagement.dto.PaiementRequestDTO;
import com.optimized.paiementmanagement.dto.PaiementResponseDTO;
import com.optimized.paiementmanagement.exception.ResourceNotFoundException;
import com.optimized.paiementmanagement.model.Paiement;
import com.optimized.paiementmanagement.repository.PaiementRepository;
import com.optimized.paiementmanagement.service.PaiementService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Payment Service Implementation - Optimized with:
 * - Constructor injection (final fields)
 * - SLF4J logging instead of System.out
 * - @Transactional for data consistency
 * - Proper exception handling
 */
@Service
@Transactional
@RequiredArgsConstructor
@Slf4j
public class PaiementServiceImpl implements PaiementService {
    
    private final PaiementRepository paiementRepository;
    
    @Override
    public PaiementResponseDTO createPaiement(PaiementRequestDTO requestDTO) {
        log.info("Creating payment for reservation: {}", requestDTO.getReservationId());
        
        // Generate unique transaction ID
        String transactionId = UUID.randomUUID().toString();
        
        Paiement paiement = Paiement.builder()
                .reservationId(requestDTO.getReservationId())
                .montant(requestDTO.getMontant())
                .datePaiement(requestDTO.getDatePaiement() != null ? 
                             requestDTO.getDatePaiement() : LocalDateTime.now())
                .modePaiement(requestDTO.getModePaiement())
                .status(Paiement.PaiementStatus.PENDING)
                .transactionId(transactionId)
                .build();
        
        Paiement savedPaiement = paiementRepository.save(paiement);
        
        log.info("Payment created successfully with transaction ID: {}", transactionId);
        
        return mapToResponseDTO(savedPaiement);
    }
    
    @Override
    @Transactional(readOnly = true)
    public PaiementResponseDTO getPaiementById(Long id) {
        log.debug("Fetching payment by ID: {}", id);
        
        Paiement paiement = paiementRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Paiement", "id", id));
        
        return mapToResponseDTO(paiement);
    }
    
    @Override
    @Transactional(readOnly = true)
    public List<PaiementResponseDTO> getAllPaiements() {
        log.debug("Fetching all payments");
        
        return paiementRepository.findAll().stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }
    
    @Override
    @Transactional(readOnly = true)
    public List<PaiementResponseDTO> getPaiementsByReservationId(Long reservationId) {
        log.debug("Fetching payments for reservation: {}", reservationId);
        
        return paiementRepository.findByReservationId(reservationId).stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }
    
    @Override
    @Transactional(readOnly = true)
    public List<PaiementResponseDTO> getPaiementsByDateRange(LocalDateTime startDate, LocalDateTime endDate) {
        log.debug("Fetching payments between {} and {}", startDate, endDate);
        
        return paiementRepository.findByDateRange(startDate, endDate).stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }
    
    @Override
    public PaiementResponseDTO updatePaiementStatus(Long id, Paiement.PaiementStatus status) {
        log.info("Updating payment {} status to {}", id, status);
        
        Paiement paiement = paiementRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Paiement", "id", id));
        
        paiement.setStatus(status);
        Paiement updatedPaiement = paiementRepository.save(paiement);
        
        log.info("Payment status updated successfully");
        
        return mapToResponseDTO(updatedPaiement);
    }
    
    @Override
    public void deletePaiement(Long id) {
        log.info("Deleting payment: {}", id);
        
        if (!paiementRepository.existsById(id)) {
            throw new ResourceNotFoundException("Paiement", "id", id);
        }
        
        paiementRepository.deleteById(id);
        
        log.info("Payment deleted successfully");
    }
    
    private PaiementResponseDTO mapToResponseDTO(Paiement paiement) {
        return PaiementResponseDTO.builder()
                .id(paiement.getId())
                .reservationId(paiement.getReservationId())
                .montant(paiement.getMontant())
                .datePaiement(paiement.getDatePaiement())
                .status(paiement.getStatus().name())
                .modePaiement(paiement.getModePaiement())
                .transactionId(paiement.getTransactionId())
                .createdDate(paiement.getCreatedDate())
                .build();
    }
}
