package com.optimized.paiementmanagement.dto;

import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

/**
 * Bank Account Request DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompteBancaireRequestDTO {
    
    @NotBlank(message = "Account number is required")
    @Pattern(regexp = "^[A-Z0-9]{10,34}$", message = "Invalid account number format")
    private String numeroCompte;
    
    @NotNull(message = "Initial balance is required")
    @DecimalMin(value = "0.00", message = "Balance must be non-negative")
    @Digits(integer = 15, fraction = 2, message = "Invalid balance format")
    private BigDecimal solde;
    
    @NotBlank(message = "Account holder name is required")
    @Size(max = 100, message = "Name must not exceed 100 characters")
    private String titulaire;
    
    @NotBlank(message = "Account type is required")
    @Size(max = 20, message = "Account type must not exceed 20 characters")
    private String typeCompte;
}
