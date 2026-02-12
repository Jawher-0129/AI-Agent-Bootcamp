package com.optimized.paiementmanagement.service;

import com.optimized.paiementmanagement.dto.CompteBancaireRequestDTO;
import com.optimized.paiementmanagement.dto.CompteBancaireResponseDTO;

import java.math.BigDecimal;
import java.util.List;

/**
 * Bank Account Service Interface
 */
public interface CompteBancaireService {
    
    CompteBancaireResponseDTO createCompte(CompteBancaireRequestDTO requestDTO);
    
    CompteBancaireResponseDTO getCompteById(Long id);
    
    CompteBancaireResponseDTO getCompteByNumero(String numeroCompte);
    
    List<CompteBancaireResponseDTO> getAllComptes();
    
    CompteBancaireResponseDTO updateSolde(Long id, BigDecimal nouveauSolde);
    
    void deleteCompte(Long id);
}
